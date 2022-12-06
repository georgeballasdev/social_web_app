from django.db import models
from django.contrib.auth.models import User

class PostModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    img = models.ImageField(upload_to='images/', blank= True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)
