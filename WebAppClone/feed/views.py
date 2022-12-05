from django.shortcuts import HttpResponse, render
from .models import PostModel

def homeview(request):
    posts = PostModel.objects.all().order_by('-created_at')[:10]
    context = {'posts': posts}
    return render(request, 'feed/home.html', context)