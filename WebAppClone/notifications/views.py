from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Notification


@login_required
def home(request):
    context = {'notifications': Notification.objects.filter(user=request.user)[::-1]}
    return render(request, 'notifications/home.html', context)

@login_required
def get_notifications(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.GET['username'])
        count = Notification.get_unseen_count(user=user)
        notifications = Notification.get_5_recent(user=user)
        list = [[x.get_link(), x.text, naturaltime(x.timestamp)] for x in notifications]
        response = {'count': count, 'list': list}
        return JsonResponse(response)
