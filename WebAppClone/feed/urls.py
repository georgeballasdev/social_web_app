from django.urls import path
from .views import homeview, PostDetailView


app_name = 'feed'
urlpatterns = [
    path('', homeview, name='home'),
    path('post/<int:id>/', PostDetailView.as_view(), name='post'),
]