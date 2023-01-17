from django.urls import path
from . import views


app_name = 'notifications'
urlpatterns = [
    path('', views.home, name='home'),
]