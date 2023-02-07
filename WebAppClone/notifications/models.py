from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.urls import reverse


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications_channel = models.CharField(max_length=150, default='')
    status_channel = models.CharField(max_length=150, default='')
    online_status = models.BooleanField(default=False)

    def get_active_client_friends_status_channels(self):
        friends = self.user.profile.friends.all()
        active = Client.objects.filter(user__in=friends, online_status=True)
        return [client.status_channel for client in active]

    def __str__(self):
        return f'Client for user {self.user.username}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    model_type = models.CharField(max_length=10)
    model_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def get_link(self):
        if self.model_type == 'post':
            return reverse('feed:post', args=[self.model_id])
        elif self.model_type == 'profile':
            return reverse('users:other_profile', args=[self.model_id])
        else:
            return 'chat'

    def get_5_recent(user):
        return Notification.objects.filter(user=user).filter(seen=False).order_by('-timestamp').all()[:5]

    def get_unseen_count(user):
        return Notification.objects.filter(user=user).filter(seen=False).count()

    def serialized(self):
        return {
            'id': self.id,
            'text': self.text,
            'link': self.get_link(),
            'timestamp': str(naturaltime(self.timestamp)),
        }

    def __str__(self):
        return f'Notification for {self.model_type} model with id {self.model_id}'