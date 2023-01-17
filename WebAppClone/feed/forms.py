from django.forms import ModelForm
from .models import Comment, Post


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'img']

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']