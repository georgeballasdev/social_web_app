import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)
        await self.accept()

    async def send_notification(self, data):
        await self.send(json.dumps(data))