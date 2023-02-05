from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage


@login_required
def get_next_messages(request):
    if request.method == 'POST':
        id = request.POST['id']
        latest_message = ChatMessage.objects.get(id=id)
        messages = latest_message.get_next_n_recent_messages()
        serialized_messages = [message.serialized() for message in messages]
        return JsonResponse({'messages': serialized_messages})
