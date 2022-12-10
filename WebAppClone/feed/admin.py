from django.contrib import admin
from .models import CommentModel, PostModel

# Register your models here.
admin.site.register(PostModel)
admin.site.register(CommentModel)