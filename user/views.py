from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import Profile, FollowerCount
from blog.models import Post,Comment
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm



def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User DOES not exist')
            return redirect('login')
           
        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'User or Password DOES not Exist')
            return redirect('login')
              
    else:
        return render(request, 'user/login.html')


@login_required(login_url='login')
def logoutView(requset):
    logout(requset)
    return redirect('login')


def register(request):
    skip_registration = request.GET.get('skip_registration', None)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exist')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username Already Exist')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id=user_model.id)
                new_profile.save()
                login(request, user)
                return redirect('setting') + '?skip_registration=True'
        else:
            messages.error(request, "Passwords Don't Match")
            return redirect('register')
    else:    
        return render(request, 'user/register.html')

@login_required(login_url='login')
def settings(request):
    skip_registration = request.GET.get('skip_registration', None)
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('avatar') == None:
            avatar = profile.avatar
            name = request.POST.get('name')
            email = request.POST.get('email')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            profession = request.POST.get('profession')

            profile.avatar = avatar
            request.user.email = email
            profile.name = name
            profile.bio = bio
            profile.location = location
            profile.profession = profession
            request.user.save()
            profile.save()
            messages.success(request, 'User Successfully Updated')
            return redirect('profile',pk=request.user)
            
            

        elif request.FILES.get('avatar') != None:
            avatar = request.FILES.get('avatar')
            name = request.POST.get('name')
            email = request.POST.get('email')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            profession = request.POST.get('profession')

            profile.avatar = avatar
            request.user.email = email
            profile.name = name
            profile.bio = bio
            profile.location = location
            profile.profession = profession
            request.user.save()
            profile.save()
            messages.success(request, 'User Successfully Updated')
            return redirect('profile',pk=request.user)
            

        else:
            messages.error(request, 'An error Occured')
            return render('setting')
        
    
        
    else:  
        context =  {'profile':profile,'skip_registration':skip_registration}  
        return render(request, 'user/setting.html', context)


@login_required(login_url='login')
def profile(request,pk):
    user_profile = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user_profile)
    posts = Post.objects.filter(author=user_profile)
    post_count = posts.count()
    post_list = Post.objects.filter(author=user_profile)[:2]
    comments = Comment.objects.filter(user=request.user).first()
    is_following = False

    followers = profile.followers.all()
    for follower in followers:
        if follower == request.user:
            is_following = True
            
    followers_list = profile.followers.all()[:5]
    number_of_followers = followers.count()
    following = profile.following.count()
    following_list = profile.following.all()[:5]

    
    cxt = {'profile':profile, 'user_profile': user_profile, 'post_count': post_count,'posts':post_list,
           'comments':comments,'is_following':is_following,'followers':followers,
           'number_of_followers':number_of_followers,'following':following,'following_list':following_list,
           'followers_list':followers_list}
    
    return render(request, 'user/user_profile.html', cxt)


@login_required(login_url='login')
def followuser(request,pk):
    user = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user)
    if user != request.user:
        profile.followers.add(request.user)
        request.user.profile.following.add(user)
    else:
        return redirect('profile', pk=user.username)
    return redirect('profile', pk=user.username)


@login_required(login_url='login')
def unfollowuser(request,pk):
    user = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user)
    profile.followers.remove(request.user)
    request.user.profile.following.remove(user)
    return redirect('profile', pk=user.username)


@login_required(login_url='login')
def followers(request, pk):
    user_profile = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user_profile)
    followers = profile.followers.all()
    cxt = {'followers':followers}
    return render(request, 'user/followers.html', cxt)


@login_required(login_url='login')
def following(request, pk):
    user_profile = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user_profile)
    following = profile.following.all()
    cxt = {'following':following}
    return render(request, 'user/following.html', cxt)


@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Password Successfully Updated")
            return redirect('profile', pk=request.user)
        else:
            messages.warning(request, "Current Password Incorrect or Passwords Didn't Match")
            return redirect('change-password')
       
    else:
        form = PasswordChangeForm(request.user) 
    return render(request, 'user/change_password.html',{'form':form})

