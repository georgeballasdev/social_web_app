from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .forms import PostCreateForm
from .models import Comment, Post


@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')[:10]
    context = {'posts': posts}
    return render(request, 'feed/home.html', context)

def comments_view(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        Comment.objects.create(
            owner=request.user,
            of_post=post,
            text=request.POST['comment']
            )
        comments = [(f'{p.owner.username}: ' , p.text) for p in post.comment_set.all()]
        return JsonResponse({"comments": comments})

def likes_view(request):
    if request.method == 'POST':
        command = request.POST['command']
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        if command == 'Like':
            post.liked_by.add(request.user)
            command = 'Unlike'
        else:
            post.liked_by.remove(request.user)
            command = 'Like'
        likes_count = post.liked_by.all().count()
        return JsonResponse({"likes_count": likes_count, "command": command})

class PostCreateView(LoginRequiredMixin, CreateView):
     def get(self, request):
        context = {'form': PostCreateForm()}
        return render(request, 'feed/post_create.html', context)

     def post(self, request):
         form = PostCreateForm(request.POST, request.FILES)
         if form.is_valid():
             post = form.save(commit=False)
             post.owner = request.user
             post.save()
             return HttpResponseRedirect(reverse_lazy('feed:home'))
         return render(request, 'feed/post_create.html', {'form': form})

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'feed/post_detail.html'

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['id'])