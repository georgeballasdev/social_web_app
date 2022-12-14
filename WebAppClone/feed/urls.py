from django.urls import path
from . import views


app_name = 'feed'
urlpatterns = [
    path('', views.homeview, name='home'),
    path('post/<int:id>/', views.PostDetailView.as_view(), name='post'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:id>/like/', views.like_view, name='like'),
    path('post/<int:id>/unlike/', views.unlike_view, name='unlike'),
]