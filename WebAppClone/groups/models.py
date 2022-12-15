from django.db import models
from django.contrib.auth.models import User
from feed.models import PostModel

class Group(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    members = models.ManyToManyField(User, related_name='members')

class GroupPost(PostModel):
    of_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_posts')