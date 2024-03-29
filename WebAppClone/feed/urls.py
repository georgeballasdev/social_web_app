from django.urls import path
from . import views


app_name = 'feed'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/ajax/comments/', views.comments_view, name='comments'),
    path('post/ajax/likes/', views.likes_view, name='likes'),
    path('post/ajax/next-posts', views.get_next_posts, name='next_posts'),
    path('post/<int:id>/', views.PostDetailView.as_view(), name='post'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
]