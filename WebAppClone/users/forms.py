from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']