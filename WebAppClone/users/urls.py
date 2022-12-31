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
    path('profile/befriend/<int:id>/', views.befriend_view, name='befriend'),
    path('profile/unfriend/<int:id>/', views.unfriend_view, name='unfriend'),
    path('ajax/getfriendsstatus/', views.getFriendsStatus, name='get_friends_status'),
]