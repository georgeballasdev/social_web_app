from django.forms import ModelForm
from .models import PostModel

class PostCreateForm(ModelForm):
    class Meta:
        model = PostModel
        fields =['text', 'img'] 