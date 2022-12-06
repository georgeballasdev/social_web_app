from django.urls import path
from .views import homeview


app_name = 'feed'
urlpatterns = [
    path('', homeview, name='home'),
]