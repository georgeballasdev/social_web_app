from django.urls import reverse
from notifications.signals import send_notification


def handle_add(user, other_user):
    if user in other_user.profile.requested_friends.all():
        user.profile.friends.add(other_user)
        other_user.profile.friends.add(user)
        send_notification(
            other_user.username,
            f'You are now friends with {user.username}',
            reverse('users:other_profile', args=[user.id])
            )
        return 'UNFRIEND'
    else:
        user.profile.requested_friends.add(other_user)
        send_notification(
            other_user.username,
            f'You have a new friend request from {user.username}',
            reverse('users:other_profile', args=[user.id])
            )
        return 'CANCEL REQUEST'

def handle_unfriend(user, other_user):
    if other_user in user.profile.friends.all():
        user.profile.friends.remove(other_user)
        other_user.profile.friends.remove(user)
    return 'ADD FRIEND'

def handle_cancel(user, other_user):
    if other_user in user.profile.friends.all():
        return 'UNFRIEND'
    else:
        user.profile.requested_friends.remove(other_user)
        return 'ADD FRIEND'

def handle_accept(user, other_user):
    if user in other_user.profile.requested_friends.all():
        user.profile.friends.add(other_user)
        other_user.profile.friends.add(user)
        other_user.profile.requested_friends.remove(user)
        send_notification(
            other_user.username,
            f'You are now friends with {user.username}',
            reverse('users:other_profile', args=[user.id])
            )
        return 'UNFRIEND'
    else:
        return 'ADD FRIEND'