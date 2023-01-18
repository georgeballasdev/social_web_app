from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return f'Notification for {self.model_type} model with id {self.model_id}'