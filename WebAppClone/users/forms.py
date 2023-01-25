from django.contrib.auth.models import User
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

class RegisterForm(forms.ModelForm):
    bio = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']