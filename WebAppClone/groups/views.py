from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from feed.models import Post
from users.models import User
from .models import Group
from .views_helpers import *


class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'groups/create.html'
    fields = ['title', 'info', 'img']
    
    def get_success_url(self):
        return reverse('groups:group', kwargs={'id':self.object.id})
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        self.object.members.add(self.request.user)
        self.request.user.profile.groups.add(self.object)
        return super().form_valid(form)
        
class GroupDetail(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'groups/detail.html'

    def get_object(self):
        return get_object_or_404(Group, id=self.kwargs['id'])

class GroupPostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'feed/post_create.html'
    fields = ['text', 'img']

    def get_success_url(self):
        return reverse('groups:group', kwargs={'id':self.object.of_group.id})
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.of_group = get_object_or_404(Group, id=self.kwargs['id'])
        self.object.save()
        return super().form_valid(form)

class GroupUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'groups/update.html'
    fields = ['info', 'img']

    def form_valid(self, form):
        profile = self.request.user.profile
        profile.info_message = 'Group updated'
        profile.save()
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Group, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('groups:group', kwargs={'id': self.kwargs['id']})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.owner:
            return redirect('groups:group', id=self.object.id)
        return super(GroupUpdate, self).dispatch(
            request, *args, **kwargs)

@login_required
def group_delete(request, id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=id)
        user = request.user
        if request.user == group.owner:
            group.delete()
            return redirect('feed:home')
    return redirect('groups:group', id=id)

@login_required
def handle_membership(request, id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=id)
        user = request.user
        command = request.POST['command']
        commands = {
            'JOIN GROUP': handle_join,
            'CANCEL REQUEST': handle_cancel,
            'LEAVE GROUP': handle_leave
        }
        response = {'state' : commands[command](group, user)}
        return JsonResponse(response)

@login_required
def handle_member(request, id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=id)
        if request.user != group.owner:
            return
        user_id = request.POST['id']
        user = get_object_or_404(User, id=user_id)
        command = request.POST['command']
        commands = {
            'APPROVE': handle_approve,
            'DISAPPROVE': handle_disapprove,
            'KICK': handle_kick,
        }
        response = {'state' : commands[command](group, user)}
        return JsonResponse(response)

@login_required
def manage_members(request, id):
    if request.method == 'GET':
        group = get_object_or_404(Group, id=id)
        if request.user == group.owner:
            return render(request, 'groups/manage.html', {'group': group})
    return redirect('groups:group', id=id)