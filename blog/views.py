from django.shortcuts import render,get_object_or_404,redirect
from .models import Category, Comment, FeaturePost,Post
from django.views.generic import DetailView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from user.models import Profile
from django.db.models import Q
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import os
from docx2pdf import convert
from django.conf import settings
from django.http import Http404,HttpResponse
from django.views import View
from django.core.paginator import Paginator




def index(request):
    feature = FeaturePost.objects.order_by('-created').first()
    post = Post.objects.all()
    posts_per_page = 10
    paginator = Paginator(post, posts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    latest_post = Post.objects.order_by('-updated')[:5]
    category = Category.objects.all()[0:11]
    cxt = {'page':page,'posts': post,'feature': feature,'category': category,'latest_post': latest_post}
    return render(request, 'blog/index.html',cxt)



def searchPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = Profile.objects.filter(
        Q(user__username__icontains=q)|
        Q(name__icontains=q)|
        Q(location__icontains=q)|
        Q(profession__icontains=q)
    )
    posts = Post.objects.filter(
        Q(category__name__icontains=q)|
        Q(title__icontains=q)|
        Q(content__icontains=q)
    )
    post_count = posts.count()
    posts_per_page = 5
    pagintor = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page = pagintor.get_page(page_number)
    cxt = {'posts': posts, 'page': page,'user':user,'post_count':post_count}
    return render(request, 'blog/search.html', cxt)



def featurePost(request, pk):
    object = FeaturePost.objects.get(id=pk)
    post_comments = object.comment_set.all().order_by('-created')
    comment_count = post_comments.count()
    latest_category = Category.objects.all()[:7]
    latest_post = Post.objects.order_by('-updated')[:3]
    post_per_page = 5
    paginator = Paginator(post_comments, post_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            feature_post = object,
            body = request.POST.get('body')
        )
        return redirect('feature', pk=object.id)
    cxt = {'object':object, 'comment_count':comment_count,
           'latest_category':latest_category,'latest_post':latest_post,'page':page}
    return render(request, 'blog/featurepost_detail.html', cxt)



@login_required(login_url='login')
def updatePost(request,pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse('You Are not Allowed Here')
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            post.title = request.POST.get('title')
            post.image = post.image
            category_name = request.POST.get('category')
            category,created = Category.objects.get_or_create(name=category_name)
            post.category = category
            post.content = request.POST.get('content')
            post.save()
            return redirect('post',pk=post.id)
        else:
            post.title = request.POST.get('title')
            post.image = request.FILES.get('image')
            category_name = request.POST.get('category')
            category,created = Category.objects.get_or_create(name=category_name)
            post.category = category
            post.content = request.POST.get('content')
            post.save()
            return redirect('post',pk=post.id)
    else:
        return render(request, 'blog/post_form.html',{'post':post})



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required(login_url='login')
def deleteView(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse('<h1>You Are Not Allowed Here</h1>')
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'blog/post_confirm_delete.html',{'post':post})



def postDetail(request, pk):
    object = Post.objects.get(id=pk)
    post_comments = object.comment_set.all().order_by('-created')
    comment_count = post_comments.count()
    latest_category = Category.objects.all()[:7]
    latest_post = Post.objects.order_by('-updated')[:3]
    post_per_page = 5
    paginator = Paginator(post_comments, post_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            post = object,
            body = request.POST.get('body')
        )
        return redirect('post', pk=object.id)
    context = {'object': object,'page': page, 'comment_count': comment_count, 
               'latest_post':latest_post,'latest_category':latest_category} 
    return render(request, 'blog/post_detail.html', context)



def categoryPage(request, name):
    category = get_object_or_404(Category, id=name)
    category_list = Category.objects.all()[:11]
    posts = Post.objects.filter(category=category)
    post_count = posts.count()
    posts_per_page = 5
    pagintor = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page = pagintor.get_page(page_number)
    cxt = {'posts': posts,'page':page,'category': category,'category_list':category_list, 'post_count': post_count}
    return render(request, 'blog/category.html', cxt)



@login_required(login_url='login')
def postCreate(request):
    category = Category.objects.all()
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            
            Post.objects.create(
                author = request.user,
                category = category,
                title = request.POST.get('title'),
                content = request.POST.get('content'),
                image = request.FILES.get('image'),
            )
            messages.success(request, "Post successfully Created")
            return redirect('index')
        except:
            messages.error(request, 'An Error occured, please try again')
            return redirect('post-create')
    else:
        messages.info(request, """
Note: You have to Select an Image that would serve as The Cover for the post
""")
        return render(request, 'blog/post_form.html')



