from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse_lazy
from .forms import PostCreateForm
from .models import PostModel


@login_required
def homeview(request):
    posts = PostModel.objects.all().order_by('-created_at')[:10]
    context = {'posts': posts}
    return render(request, 'feed/home.html', context)

@login_required
def like_view(request, id):
    if request.method == 'POST':
        post = get_object_or_404(PostModel, id=id)
        post.liked_by.add(request.user)
    return HttpResponseRedirect(reverse_lazy('feed:home'))

@login_required
def unlike_view(request, id):
    if request.method == 'POST':
        post = get_object_or_404(PostModel, id=id)
        post.liked_by.remove(request.user)
    return HttpResponseRedirect(reverse_lazy('feed:home'))

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
    model = PostModel
    template_name = 'feed/post_detail.html'

    def get_object(self):
        return get_object_or_404(PostModel, id=self.kwargs['id'])