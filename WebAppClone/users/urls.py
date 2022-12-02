from django.urls import include, path
from .views import ProfileView, UserLoginView, welcomeview

app_name = 'users'
urlpatterns = [
    path('', welcomeview, name='welcome'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:id>', ProfileView.as_view(), name='profile'),
]