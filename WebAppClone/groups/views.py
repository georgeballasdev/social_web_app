from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from .models import Group, GroupPost


class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'groups/create.html'
    fields = ['title', 'info']
    
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
    model = GroupPost
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

    def get_object(self):
        return get_object_or_404(Group, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse('groups:group', kwargs={'id': self.kwargs['id']})

@login_required
def handle_join(request, id):
    return JsonResponse({'ok':'ok'})
    # if request.method == 'POST':
    #     user = request.user
    #     other_user = get_object_or_404(User, id=id)
    #     command = request.POST['command']
    #     commands = {
    #         'ADD FRIEND': handle_add,
    #         'UNFRIEND': handle_unfriend,
    #         'CANCEL REQUEST': handle_cancel,
    #         'ACCEPT REQUEST': handle_accept,
    #     }
    #     response = {'state' : commands[command](user, other_user)}
    #     return JsonResponse(response)