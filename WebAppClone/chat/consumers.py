import json
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user'].username

        if user != self.scope['url_route']['kwargs']['user']:
            self.disconnect('invalid user')
        friend = self.scope['url_route']['kwargs']['friend']
        if not self.valid_friend(user, friend):
            self.disconnect('invalid friend')

        self.group_name = await self.get_group_name(user, friend)
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        print('DISCONNECTED', code)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def get_messages(self, data):
        messages = await self.get_recent_messages(self.group_name)
        recent_messages = await self.messages_to_json(messages)
        data = {
            'command': 'get_messages',
            'messages': recent_messages
        }
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_recent_messages(self, group):
        return ChatMessage.get_10_recent(group)

    async def new_message(self, data):
        sender = data['sender']
        receiver = data['receiver']
        content = data['content']
        message = await self.save_and_get_message(sender, receiver, self.group_name, content)
        await self.channel_layer.group_send(
            self.group_name, {
                'type': 'chat_message',
                'message': message,
                }
        )

    commands = {
        'get_messages': get_messages,
        'new_message': new_message
    }

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)
        
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))    

    async def get_group_name(self, user, friend):
        if user < friend:
            return f'{user}-{friend}'
        else:
            return f'{friend}-{user}'

    @database_sync_to_async
    def valid_friend(self, user, friend):
        return friend in User.objects.exclude(username=user)

    @database_sync_to_async
    def save_and_get_message(self, sender, receiver, group, content):
        message = ChatMessage.objects.create(
            sender=User.objects.get(username=sender),
            receiver=User.objects.get(username=receiver),
            group=group,
            content=content
        )
        return {
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'content': message.content,
                'timestamp': str(message.timestamp)}

    @database_sync_to_async
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append({
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'content': message.content,
                'timestamp': str(message.timestamp)})
        return result