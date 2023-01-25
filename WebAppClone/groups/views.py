from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Group

@login_required
def group_page(request, id):
    group = get_object_or_404(Group, id=id)
    context = {'group': group}
    return render(request, 'groups/group_page.html', context)

class GroupList(ListView):
    model = Group
    template_name = 'groups/group_list.html'