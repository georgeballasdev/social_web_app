from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .views_helpers import *
from .forms import ProfileForm, UserForm


def welcome(request):
    if request.user.is_authenticated:
        return redirect(reverse('feed:home'))
    return redirect(reverse('users:login'))

@login_required
def profile(request, id=None):
    user = request.user
    context = {'profile_user': user}
    if id and id != user.id:
        profile_user = get_object_or_404(User, id=id)
        context['profile_user'] = profile_user
        context['friendship_button_state'] = user.profile.get_friendship_button_state(profile_user)
    return render(request, 'users/profile.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            usr = user_form.save()
            prof = profile_form.save(commit=False)
            prof.user = usr
            prof.save()
            login(request, usr)
            return redirect('users:profile')
    else:
        if request.user.is_authenticated:
            return redirect('feed:home')
        user_form = UserForm()
        profile_form = ProfileForm()
    context = {'user_form':user_form, 'profile_form': profile_form}
    return render(request, 'users/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('users:login')

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
    return redirect(reverse('feed:home'))

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    next_page = 'feed:home'
    redirect_authenticated_user = True

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update.html'
    fields = ['bio', 'pic']

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('users:profile')

def get_friends_status(request):
    response = {}
    if request.method == "GET":
        friends = request.user.friends.all()
        for friend in friends:
            response[friend.user.username] = friend.online_status
    return JsonResponse(response, status=200)