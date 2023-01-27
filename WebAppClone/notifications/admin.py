from django.contrib import admin
from .models import Client, Notification


admin.site.register([Client, Notification])
