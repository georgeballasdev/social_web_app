from django.urls import path
from .views import get_next_messages


app_name = 'chat'
urlpatterns = [
    path('ajax/next-messages', get_next_messages, name='next_messages'),
]