from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('ajax/handle-friendship/<int:id>/', views.handle_friendship, name='handle_friendship'),
    path('ajax/info-message/', views.info_message, name='info_message'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.UserPasswordChangeView.as_view(), name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>/', views.profile, name='other_profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='update'),
    path('register/', views.register, name='register'),
]