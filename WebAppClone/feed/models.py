from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.urls import reverse
from groups.models import Group


def group_pic_path(instance, filename):
    return f'images/post-pics/{instance.owner.username}/{filename}'

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    img = models.ImageField(upload_to=group_pic_path, blank= True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_by', blank=True)
    of_group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE, related_name='posts')

    def serialized(self, user):
        comments_query = self.comment_set.all().order_by('-created_at')
        comments = []
        for comment in comments_query:
            comments.insert(0, {
                'pic': comment.owner.profile.pic.url,
                'profile_url': reverse('users:other_profile', args=[comment.owner.id]),
                'user': comment.owner.username,
                'text': comment.text,
                'timestamp': str(naturaltime(comment.created_at))
            })
        post = {
            'id': self.id,
            'pic': self.owner.profile.pic.url,
            'post_url': 'test',
            'profile_url':'test',
            'owner': self.owner.username,
            'text': self.text,
            'img': self.img.url if self.img else '',
            'timestamp': str(naturaltime(self.created_at)),
            'likes': self.liked_by.count(),
            'liked': user in self.liked_by.all(),
            'comments': comments
        }
        return post

class Comment(models.Model):
    of_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)