from django.urls import re_path
from .consumers import ChatConsumer, NotificationsConsumer, StatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user>\w+)-(?P<friend>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/', NotificationsConsumer.as_asgi()),
    re_path(r'ws/status/', StatusConsumer.as_asgi()),
]