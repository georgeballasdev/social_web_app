import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Client, Notification


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Update Client
        user = self.scope['user']
        await update_client(user, notifications_channel=self.channel_name)
        # Accept connection
        await self.accept()

    async def send_notification(self, data):
        await self.send(json.dumps(data))

    async def receive(self, text_data):
        count = await self.mark_unseen(json.loads(text_data))
        await self.send(json.dumps({"count": count}))

    @database_sync_to_async
    def mark_unseen(self, data):
        for id in data['seen']:
            obj = Notification.objects.get(id=int(id))
            obj.seen = True
            obj.save()
        return Notification.get_unseen_count(self.scope['user'])
        

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        # Resend offline status in case beaforeunload fails
        await update_client(
                self.scope['user'],
                online_status=False
            )
        self.close()

    async def receive(self, text_data=None, byte_data=None):
        if text_data:
            data = json.loads(text_data)
            await update_client(
                self.scope['user'],
                online_status=data['status'],
                status_channel=self.channel_name
            )

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
    if status_channel:
        client.status_channel = status_channel
    client.save()