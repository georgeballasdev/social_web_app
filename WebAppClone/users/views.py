from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


def welcomeview(request):
    user = request.user.is_authenticated
    if user:
        return redirect(reverse('feed:home'))
    return redirect(reverse('users:login'))

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, id):
        model = get_user_model()
        try:
            user = model.objects.get(id=id)
            return render(request, 'users/profile.html')
        except model.DoesNotExist:           
            return render(request, 'users/fail.html')

class UserLoginView(LoginView):
    # Note: Problems with login, user doesn't change and unathenticated users go 404
    template_name = 'users/login.html'

    def form_valid(self, form):
        user_id = str(form.get_user().id)
        return HttpResponseRedirect(reverse('users:profile', args=(user_id,)))
