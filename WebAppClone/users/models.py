from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from feed.models import Post
from groups.models import Group
from random import choice


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    pic = models.ImageField(upload_to='images/pics/', default='/images/no_pic.jpeg')
    joined_at = models.DateField(auto_now_add=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    requested_friends = models.ManyToManyField(User, related_name='requested_friends', blank=True)
    latest_posts_query = models.ManyToManyField(Post, related_name='latest_posts_query', blank=True)
    groups = models.ManyToManyField(Group, related_name='groups', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_friendship_button_state(self, other_user):
        if other_user in self.friends.all():
            return 'UNFRIEND'
        if other_user in self.requested_friends.all():
            return 'CANCEL REQUEST'
        if self.user in other_user.profile.requested_friends.all():
            return 'ACCEPT REQUEST'
        return 'ADD FRIEND'

    def update_latest_posts(self):
        own_posts = Post.objects.filter(owner=self.user)
        friends_posts = Post.objects.filter(owner__in=self.friends.all())
        self.latest_posts_query.set(own_posts.union(friends_posts))

    def get_next_n_recent_posts(self, iteration=0):
        start = iteration * settings.RECENT_POSTS_N
        end = iteration * settings.RECENT_POSTS_N + settings.RECENT_POSTS_N
        return self.latest_posts_query.order_by('-created_at')[start:end]

    def get_owned_groups(self):
        return self.groups.filter(owner=self.user).order_by('title')

    def get_joined_groups(self):
        return self.groups.exclude(owner=self.user).order_by('title')

    def get_random_group(self):
        all_pks = Group.objects.values_list('pk', flat=True)
        member_pks = self.groups.values_list('pk', flat=True)
        not_member_pks = all_pks.difference(member_pks)
        random_pk = choice(not_member_pks)
        return Group.objects.get(pk=random_pk)