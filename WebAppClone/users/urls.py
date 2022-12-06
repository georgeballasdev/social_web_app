from django.urls import include, path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('profile/<int:id>', views.ProfileView.as_view(), name='profile'),
]