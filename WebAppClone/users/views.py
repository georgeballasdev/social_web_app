from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from .forms import ProfileForm, UserForm


def welcome(request):
    user = request.user.is_authenticated
    if user:
        return redirect(reverse('feed:home'))
    return redirect(reverse('users:login'))

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        model = User
        try:
            user = model.objects.get(id=id)
            return render(request, 'users/profile.html')
        except model.DoesNotExist:           
            return render(request, 'users/fail.html')

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
            return redirect('users:profile', usr.id)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    context = {'user_form':user_form, 'profile_form': profile_form}
    return render(request, 'users/register.html', context)


class UserLoginView(LoginView):
    # Note: Problems with login, user doesn't change and unathenticated users go 404
    template_name = 'users/login.html'

    def form_valid(self, form):
        user_id = str(form.get_user().id)
        return redirect('users:profile',user_id)
