from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from feed.models import Post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    pic = models.ImageField(upload_to='images/pics/', default='/images/no_pic.jpeg')
    joined_at = models.DateField(auto_now_add=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    requested_friends = models.ManyToManyField(User, related_name='requested_friends', blank=True)
    latest_posts_query = models.ManyToManyField(Post, related_name='latest_posts_query', blank=True)

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

    def __str__(self):
        return f'Profile of {self.user.username}'
