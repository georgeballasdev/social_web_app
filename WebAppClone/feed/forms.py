from django.forms import ModelForm
from .models import CommentModel, PostModel


class PostCreateForm(ModelForm):
    class Meta:
        model = PostModel
        fields = ['text', 'img']

class CommentCreateForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = ['text']