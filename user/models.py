from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    avatar = models.ImageField(upload_to='avatar', default='forum-author1.png')
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(User, blank=True,  related_name='followers')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    location = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.username



class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    follower_profile =  models.OneToOneField(Profile, on_delete=models.CASCADE,null=True)


