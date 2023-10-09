from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutView, name='logout'),

    path('setting/', views.settings, name='setting'),
    path('change-password/', views.changePassword, name='change-password'),
    path('profile/<str:pk>', views.profile, name='profile'),

    path('profile/<str:pk>/followers/add/', views.followuser, name='followuser'),
    path('profile/<str:pk>/followers/remove/', views.unfollowuser, name='unfollowuser'),

    path('profile/<str:pk>/followers', views.followers, name='followers'),
    path('profile/<str:pk>/following', views.following, name='following'),
    
]