from django.urls import path
from . import views


app_name = 'groups'
urlpatterns = [
    path('<int:id>/', views.group_page, name='group_page'),
]