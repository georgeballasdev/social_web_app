from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    pic = models.ImageField(upload_to='images/pics/', default='/images/no_pic.jpeg')
    joined_at = models.DateField(auto_now_add=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    requested_friends = models.ManyToManyField(User, related_name='requested_friends', blank=True)

    def get_friendship_button_state(self, other_user):
        if other_user in self.friends.all():
            return 'UNFRIEND'
        if other_user in self.requested_friends.all():
            return 'CANCEL REQUEST'
        if self.user in other_user.profile.requested_friends.all():
            return 'ACCEPT REQUEST'
        return 'ADD FRIEND'

    def __str__(self):
        return f'Profile of {self.user.username}'
