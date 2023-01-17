from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    img = models.ImageField(upload_to='images/pics', blank= True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name='liked_by', blank=True)

class Comment(models.Model):
    of_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)