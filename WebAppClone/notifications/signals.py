from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from feed.models import Comment, Post
from .models import Notification
from django.contrib.contenttypes.fields import GenericForeignKey


@receiver(post_save, sender=Comment)
def new_comment(sender, instance, **kwargs):
    user = instance.owner.username
    text = f'{user} commented on your post'
    notification = Notification.objects.create(
        user=instance.owner,
        text=text,
        content_type=ContentType.objects.get(model='post'),
        object_id=instance.id,
        content_object = instance
    )
    owner = instance.of_post.owner.username
    link = notification.get_link()
    send_notification(owner, text, link)

def send_notification(user, text, link):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(user, {
            "type": "send_notification",
            "text": text,
            "link": link
            })