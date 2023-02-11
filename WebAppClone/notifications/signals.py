from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from chat.models import ChatMessage
from feed.models import Comment, Post
from .models import Client, Notification


channel_layer = get_channel_layer()

@receiver(post_save, sender=Comment)
def new_comment(sender, instance, **kwargs):
    notification = Notification.objects.create(
        user = instance.of_post.owner,
        text = f'{instance.owner.username} commented on your post',
        model_type = 'post',
        model_id = instance.of_post.id
    )
    send_notification(notification)

@receiver(m2m_changed, sender='feed.Post_liked_by')
def new_like(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        print(f'In new like receiver, pk_set {list(pk_set)}')
        liker = User.objects.get(id=list(pk_set)[0]).username
        notification = Notification.objects.create(
            user = instance.owner,
            text = f'{liker} liked your post',
            model_type = 'post',
            model_id = instance.id
        )
        send_notification(notification)

@receiver(post_save, sender=ChatMessage)
def new_message(sender, instance, **kwargs):
    user = instance.receiver
    client = Client.objects.get(user=user)
    async_to_sync(channel_layer.send)(client.notifications_channel, {
        "type": "send.notification",
        "user": user.username,
        })

@receiver(post_save, sender=Post)
def new_group_post(sender, instance, created, **kwargs):
    group = instance.of_group
    if group and not created:
        for member in group.members.exclude(id=instance.owner.id).all():
            notification = Notification.objects.create(
                user = member,
                text = f'{instance.owner.username} posted in group {instance.of_group.title}',
                model_type = 'post',
                model_id = instance.id
            )
            send_notification(notification)

def send_notification(notification):
    client = Client.objects.get(user=notification.user)
    async_to_sync(channel_layer.send)(client.notifications_channel, {
        "type": "send.notification",
        "notification": notification.serialized(),
        "count": Notification.get_unseen_count(notification.user)
        })

@receiver(post_save, sender=Client)
def status_changed(sender, instance, **kwargs):
    active_channels = instance.get_active_client_friends_status_channels()
    for channel in active_channels:
        async_to_sync(channel_layer.send)(channel, {
            "type": "send.status",
            "user": instance.user.username,
            "status": instance.online_status
        })