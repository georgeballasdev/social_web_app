from django.urls import include, path
from .views import homeview


app_name = 'feed'
urlpatterns = [
    path('', homeview, name='home'),
]