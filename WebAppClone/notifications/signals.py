from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.dispatch import receiver
from chat.models import ChatMessage
from feed.models import Comment, Post
from groups.models import Group
from .models import Client, Notification

# Notifications
channel_layer = get_channel_layer()

@receiver(post_save, sender=Comment)
def new_comment(sender, instance, **kwargs):
    if instance.of_post.owner != instance.owner: # Don't notify own comment on own post
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
        liker = User.objects.get(id=list(pk_set)[0]).username
        if liker != instance.owner.username: # Don't notify own like on own post
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
        "user": instance.sender.username,
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

# Profile info_message
def update_info_message(profile, info):
    profile.info_message = info
    profile.save()

@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        update_info_message(instance.owner.profile, 'Post created')

@receiver(post_save, sender=Group)
def group_created(sender, instance, created, **kwargs):
    if created:
        update_info_message(instance.owner.profile, 'Group created')

@receiver(pre_delete, sender=Group)
def group_deleted(sender, instance, **kwargs):
    update_info_message(instance.owner.profile, 'Group deleted')