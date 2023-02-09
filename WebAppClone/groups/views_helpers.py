def handle_join(group, user):
    if user not in group.requested_members.all():
        group.requested_members.add(user)
    return 'CANCEL REQUEST'

def handle_cancel(group, user):
    if user in group.requested_members.all():
        group.requested_members.remove(user)
    return 'JOIN GROUP'

def handle_leave(group, user):
    if user in group.members.all():
        group.members.remove(user)
        user.profile.groups.remove(group)
    return 'REFRESH'

def handle_approve(group, user):
    if user not in group.members.all():
        group.requested_members.remove(user)
        group.members.add(user)
        user.profile.groups.add(group)
    return 'APPROVED'

def handle_disapprove(group, user):
    if user in group.requested_members.all():
        group.requested_members.remove(user)
    return 'DISAPPROVED'

def handle_kick(group, user):
    if user in group.members.all():
        group.members.remove(user)
        user.profile.groups.remove(group)
    return 'KICKED'