from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View
from .forms import PostCreateForm
from .models import PostModel


@login_required
def homeview(request):
    posts = PostModel.objects.all().order_by('-created_at')[:10]
    context = {'posts': posts}
    return render(request, 'feed/home.html', context)

@login_required
def like_view(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        post = get_object_or_404(PostModel, id=id)
        post.liked_by.add(request.user)
    return render(request, 'feed/home.html')

@login_required
def unlike_view(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        post = get_object_or_404(PostModel, id=id)
        post.liked_by.remove(request.user)
    return render(request, 'feed/home.html')

def getlikes(request):
    return render(request, 'feed/home.html')

class GetLikesView(LoginRequiredMixin, View):
    def get(self, request, id):
        post = get_object_or_404(PostModel, id=id)
        likes = post.liked_by.all().count()
        print(f'got post with id {id}')
        return JsonResponse(likes, safe=False)

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