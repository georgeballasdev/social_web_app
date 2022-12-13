from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    joined_at = models.DateField(auto_now_add=True)
    pic = models.ImageField(upload_to='images/pics/', default='/images/no_pic.jpeg')
