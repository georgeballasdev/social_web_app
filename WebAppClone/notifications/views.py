from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Notification


@login_required
def home(request):
    notifications = Notification.objects.filter(user=request.user)
    context = {
        'unseen': notifications.filter(seen=False).order_by('-timestamp'),
        'seen': notifications.filter(seen=True).order_by('-timestamp')
    }
    for notification in context['unseen']:
        notification.seen = True
        notification.save()
    return render(request, 'notifications/home.html', context)

@login_required
def get_notifications(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.GET['username'])
        count = Notification.get_unseen_count(user=user)
        list = [x.serialized() for x in Notification.get_5_recent(user=user)]
        response = {'count': count, 'list': list}
        return JsonResponse(response)
