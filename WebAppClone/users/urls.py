from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>/', views.profile, name='other_profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='update'),
    path('profile/add/<int:id>/', views.add_view, name='add'),
]