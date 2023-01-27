from django.urls import re_path
from .consumers import NotificationsConsumer, StatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/', NotificationsConsumer.as_asgi()),
    re_path(r'ws/status/', StatusConsumer.as_asgi()),
]