from django.urls import path
from . import views


app_name = 'feed'
urlpatterns = [
    path('', views.homeview, name='home'),
    path('post/<int:id>/', views.PostDetailView.as_view(), name='post'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/like/', views.like_view, name='like'),
    path('post/unlike/', views.unlike_view, name='unlike'),
    path('post/getlikes/', views.getlikes, name='getlikesurl'),
    path('post/getlikes/<int:id>/', views.GetLikesView.as_view(), name='getlikes'),
    path('post/add-comment/', views.add_comment_view, name='add_comment'),
    path('post/get-comments/', views.GetCommentsView.as_view(), name='get_comments'),
]