from django.urls import path
from . import views


app_name = 'feed'
urlpatterns = [
    path('', views.homeview, name='home'),
    path('post/<int:id>/', views.PostDetailView.as_view(), name='post'),
]