from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    group = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ChatMessage of {self.group} - {self.id}'

    def get_recent_messages(group):
        return ChatMessage.objects.filter(group=group).order_by('-timestamp').all()[:settings.RECENT_MESSAGES_N:-1]
    
    def get_next_n_recent_messages(self):
        return ChatMessage.objects.filter(
            group=self.group, timestamp__lt=self.timestamp
            ).order_by('-timestamp').all()[:settings.RECENT_MESSAGES_N]

    def serialized(self):
        return {
        'sender': self.sender.username,
        'receiver': self.receiver.username,
        'content': self.content,
        'timestamp': str(naturaltime(self.timestamp)),
        'id': self.id
        }