from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import ProfileForm, UserForm


def welcome(request):
    user = request.user.is_authenticated
    if user:
        return redirect(reverse('feed:home'))
    return redirect(reverse('users:login'))

@login_required
def profile(request, id=None):
    user = request.user
    context = {'profile_user': user}
    if id and id != user.id:
        profile_user = get_object_or_404(User, id=id)
        context['profile_user'] = profile_user
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

@login_required
def befriend_view(request, id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=id)
        request.user.profile.friends.add(friend)
        friend.profile.friends.add(request.user)
        return redirect(reverse('users:other_profile', args=[id,]))
    return redirect(reverse('feed:home'))

@login_required
def unfriend_view(request, id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=id)
        request.user.profile.friends.remove(friend)
        friend.profile.friends.remove(request.user)
        return redirect(reverse('users:other_profile', args=[id,]))
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

def getFriendsStatus(request):
    if request.method == "GET":
        friends = request.user.friends.all()
        response = []
        for friend in friends:
            response.append({friend.user.username: friend.online_status})
        return JsonResponse(response, status = 200, safe=False)
    return JsonResponse({}, status = 400)