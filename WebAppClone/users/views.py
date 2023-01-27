from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, UpdateView
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

class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        self.object = form.save()
        Profile.objects.create(
            user=self.object,
            bio=form['bio'].value()
        )
        Client.objects.create(
            user=self.object,
        )
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())

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