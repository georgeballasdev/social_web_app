import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Client


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Update Client
        user = self.scope['user']
        await update_client(user, notifications_channel=self.channel_name)
        # Accept connection
        await self.accept()

    async def send_notification(self, data):
        await self.send(json.dumps(data))

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Update Client
        user = self.scope['user']
        await update_client(user, online_status=True, status_channel=self.channel_name)
        # Accept connection
        await self.accept()

    async def disconnect(self, code):
        # Update client
        user = self.scope['user']
        await update_client(user, online_status=False)
        self.close()

    async def send_status(self, data):
        await self.send(json.dumps({
            "user": data["user"],
            "status": data["status"]
        }))

@database_sync_to_async
def update_client(user, online_status=None, notifications_channel=None, status_channel=None):
    client = Client.objects.get(user=user)
    if online_status != None:
        client.online_status = online_status
    if notifications_channel:
        client.notifications_channel = notifications_channel
    elif status_channel:
        client.status_channel = status_channel
    client.save()