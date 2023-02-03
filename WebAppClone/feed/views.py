from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from .models import Comment, Post


@login_required
def home_view(request):
    friends = request.user.profile.friends.all()
    own_posts = Post.objects.filter(owner=request.user)
    friends_posts = Post.objects.filter(owner__in=friends)
    posts = own_posts.union(friends_posts).order_by('-created_at')[:10]
    context = {'posts': posts}
    return render(request, 'feed/home.html', context)

@login_required
def comments_view(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(
            owner=request.user,
            of_post=post,
            text=request.POST['comment']
        )
        new_comment = {
            'user': request.user.username,
            'profile': reverse('users:other_profile', kwargs={'id': request.user.id}),
            'text': comment.text,
            'timestamp': naturaltime(comment.created_at),
            'url': request.user.profile.pic.url
        }
        return JsonResponse({'comment': new_comment})

@login_required
def likes_view(request):
    if request.method == 'POST':
        command = request.POST['command']
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        if command == 'like':
            post.liked_by.add(request.user)
            command = 'unlike'
        else:
            post.liked_by.remove(request.user)
            command = 'like'
        likes_count = post.liked_by.all().count()
        return JsonResponse({'likes_count': likes_count, 'command': command})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'feed/post_create.html'
    fields = ['text', 'img']
    success_url = reverse_lazy('feed:home')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'feed/post_detail.html'

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['id'])