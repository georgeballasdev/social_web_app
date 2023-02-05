from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from chat.models import ChatMessage
from feed.models import Comment
from .models import Client, Notification


@receiver(post_save, sender=Comment)
def new_comment(sender, instance, **kwargs):
    notification = Notification.objects.create(
        user = instance.of_post.owner,
        text = f'{instance.owner.username} commented on your post.',
        model_type = 'post',
        model_id = instance.id
    )
    user = notification.user
    text = notification.text
    link = notification.get_link()
    send_notification(user, text, link)

# @receiver(m2m_changed, sender='feed.Post_liked_by')
# def new_like(sender, instance, action, pk_set, **kwargs):
#     if action == 'post_add':
#         liker = User.objects.get(id=list(pk_set)[0]).username
#         notification = Notification.objects.create(
#             user = instance.owner,
#             text = f'{liker} liked your post.',
#             model_type = 'post',
#             model_id = instance.id
#         )
#         user = notification.user
#         text = notification.text
#         link = notification.get_link()
#         send_notification(user, text, link)

@receiver(post_save, sender=ChatMessage)
def new_message(sender, instance, **kwargs):
    user = instance.receiver
    text = f'You have a new message from {instance.sender.username}.'
    send_notification(user, text)


def send_notification(user, text, link=''):
    client = Client.objects.get(user=user)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(client.notifications_channel, {
        "type": "send.notification",
        "text": text,
        "link": link
        })

@receiver(post_save, sender=Client)
def status_changed(sender, instance, **kwargs):
    user = instance.user
    channel_layer = get_channel_layer()
    active_channels = instance.get_active_client_friends_status_channels()
    for channel in active_channels:
        async_to_sync(channel_layer.send)(channel, {
            "type": "send.status",
            "user": user.username,
            "status": instance.online_status
        })