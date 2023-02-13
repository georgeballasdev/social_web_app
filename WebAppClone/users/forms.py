from django import forms
from django.contrib.auth.models import User
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

    # Check for username and email uniqueness
    def clean_username(self):
        username = self.cleaned_data['username']
        existing_user = User.objects.filter(username=username)
        if existing_user:
            raise forms.ValidationError(f"Username {username} already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        existing_user = User.objects.filter(email=email)
        if existing_user:
            raise forms.ValidationError(f"Email {email} already exists")
        return email