from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PostModel

@login_required
def homeview(request):
    posts = PostModel.objects.all().order_by('-created_at')[:10]
    context = {'posts': posts}
    return render(request, 'feed/home.html', context)