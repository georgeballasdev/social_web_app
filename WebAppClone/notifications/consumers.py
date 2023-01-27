import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Client


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Create/Update Client
        # user = self.scope['user']
        # client = await get_client(user)
        # await update_client(user, client, notifications_channel=self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        pass

    async def send_notification(self, data):
        await self.send(json.dumps(data))

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Create/Update Client
        user = self.scope['user']
        client = await get_client(user)
        client = await update_client(user, client, status_channel=self.channel_name)
        # Get all friends clients
        active_channels = await self.get_active_channels(client)
        # Send online status
        print(f'SENDING ONLINE STATUS TO {len(active_channels)} USERS')
        for channel in active_channels:
            print(f'channel: {channel}')
            await self.channel_layer.send(channel, {
                "type": "send.status",
                "user": user.username,
                "status": "online"
            })

        await self.accept()

    async def disconnect(self, code):
        # Get client
        user = self.scope['user']
        client = await get_client(user)
        if client:
            # Get all friends clients
            active_channels = await self.get_active_channels(client)
            # Send offline status
            for channel in active_channels:
                await self.channel_layer.send(channel, {
                    "type": "send.status",
                    "user": user.username,
                    "status": "offline"
                })

        #     await delete_client(client)

    async def send_status(self, data):
        await self.send(json.dumps({
            "user": data["user"],
            "status": data["status"]
        }))

    @database_sync_to_async
    def get_active_channels(self, client):
        return client.get_active_client_friends_status_channels()

@database_sync_to_async
def get_client(user):
    return Client.objects.filter(user=user).first()

@database_sync_to_async
def update_client(user, client, notifications_channel=None, status_channel=None):
    if client == None:
        client = Client.objects.create(user=user)
    if notifications_channel:
        client.notifications_channel = notifications_channel
    elif status_channel:
        client.status_channel = status_channel
    client.save()
    return client

@database_sync_to_async
def delete_client(client):
    client.delete()