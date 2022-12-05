from django.contrib.auth import get_user_model
from django.db import models

class PostModel(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    img = models.ImageField(upload_to='images/', blank= True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)
