from django.contrib.auth.models import User
from django.db import models

def group_pic_path(instance, filename):
    return f'images/groups-pics/{instance.owner.username}/{filename}'

class Group(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()
    img = models.ImageField(upload_to=group_pic_path, default='/images/generic//no_pic.jpeg')
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='members')
    requested_members = models.ManyToManyField(User, blank=True, related_name='requestes_members')

    def get_joined_members(self):
        return self.members.exclude(id=self.owner.id)