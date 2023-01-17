from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def get_link(self):
        if 'post' in str(self.content_type):
            return reverse('feed:post', args=[self.object_id])
        else:
            return reverse('users:other_profile', args=[self.object_id])

    def __str__(self):
        return f'Notification for {self.content_object} of type {self.content_type}'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]