from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Length
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from groups.models import Group


@login_required
def search_results(request):
    if request.method == 'GET':
        query = request.GET['query']
        if 'X-Requested-With' in request.headers: # AJAX
            return JsonResponse(search(query))
        return render(request, 'search/results.html', {'results': search(query), 'query': query})

def search(query):
    users = User.objects.filter(username__istartswith=query).order_by(Length('username').asc())
    groups = Group.objects.filter(title__istartswith=query).order_by(Length('title').asc())
    return {
        'users': [
            {
                'username': user.username,
                'pic': user.profile.pic.url,
                'link': reverse('users:other_profile', args=[user.id])
            } for user in users
        ],
        'groups': [
            {
                'title': group.title,
                'link': reverse('groups:group', args=[group.id] )
            } for group in groups
        ]
    }