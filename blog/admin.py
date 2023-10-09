from django.contrib import admin
from .models import Comment, Post, FeaturePost, Article, Category

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(FeaturePost)
admin.site.register(Article)
admin.site.register(Category)



