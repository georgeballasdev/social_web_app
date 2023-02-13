from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import JsonResponse
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from notifications.models import Client
from .models import Profile
from .forms import RegisterForm
from .views_helpers import *


def welcome(request):
    return redirect(reverse('feed:home'))

@login_required
def profile(request, id=None):
    user = request.user
    context = {'profile_user': user}
    if id and id != user.id:
        profile_user = get_object_or_404(User, id=id)
        context['profile_user'] = profile_user
        context['friendship_button_state'] = user.profile.get_friendship_button_state(profile_user)
    return render(request, 'users/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def handle_friendship(request, id):
    if request.method == 'POST':
        user = request.user
        other_user = get_object_or_404(User, id=id)
        command = request.POST['command']
        commands = {
            'ADD FRIEND': handle_add,
            'UNFRIEND': handle_unfriend,
            'CANCEL REQUEST': handle_cancel,
            'ACCEPT REQUEST': handle_accept,
        }
        response = {'state' : commands[command](user, other_user)}
        return JsonResponse(response)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password']),
                email=form.cleaned_data['email']
            )
            Profile.objects.create(
                user=user,
                bio=form.cleaned_data['bio']
            )
            Client.objects.create(
                user=user,
            )
            login(request, user)
            return redirect('users:profile')
    else:
        form = RegisterForm()
    return render(request, 'users/enter.html', {'form': form, 'register': True})

class UserLoginView(LoginView):
    template_name = 'users/enter.html'
    next_page = 'feed:home'
    redirect_authenticated_user = True

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update.html'
    fields = ['bio', 'pic']

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('users:profile')

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:profile')