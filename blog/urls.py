from django.urls import path
from . import views
from .views import PostDeleteView

urlpatterns = [
    path('', views.index, name='index'),
    path('feature/<str:pk>/', views.featurePost, name='feature'),
    path('post/<str:pk>/', views.postDetail, name='post'),
    path('search/', views.searchPage, name='search'),
    path('category/<str:name>/', views.categoryPage, name='category'),
    path('post/<str:pk>/update/', views.updatePost, name='post-update'),
    path('post/<str:pk>/delete/', views.deleteView, name='post-delete'),
    path('post-create/', views.postCreate, name='post-create'),
]