def handle_add(user, other_user):
    if user in other_user.profile.requested_friends.all():
        user.profile.friends.add(other_user)
        other_user.profile.friends.add(user)
        # send befriended notification to other_user
        return 'UNFRIEND'
    else:
        user.profile.requested_friends.add(other_user)
        # send friend request notification to other_user
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
        # send befriended notification to other_user
        return 'UNFRIEND'
    else:
        return 'ADD FRIEND'