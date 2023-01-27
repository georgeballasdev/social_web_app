from django.contrib.auth.models import User
from django import forms
from .models import Profile


class RegisterForm(forms.ModelForm):
    bio = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']