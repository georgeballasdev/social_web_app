from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def home(request):
    context = {'notifications': Notification.objects.all()}
    return render(request, 'notifications/home.html', context)
