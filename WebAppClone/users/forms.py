from django import forms
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=4,
        required=True,
        label='Username',
        help_text='Pick a unique username'
    )
    password = forms.CharField(
        min_length=6,
        validators=[validate_password],
        required=True,
        label='Password',
        help_text='Pick a complex password',
        widget=forms.PasswordInput()
    )
    email = forms.EmailField(
        required=True,
        help_text='Input your email'
    )
    bio = forms.CharField(
        max_length=500,
        required=False,
        help_text='Optional bio for your profile',
    )