from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render
from .models import PostModel

@login_required
def homeview(request):
    posts = PostModel.objects.all().order_by('-created_at')[:10]
    context = {'posts': posts}
    return render(request, 'feed/home.html', context)

class PostDetailView(DetailView):
    model = PostModel
    template_name = 'feed/post_detail.html'

    def get_object(self):
        return get_object_or_404(PostModel, id=self.kwargs['id'])