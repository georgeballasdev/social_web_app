from django.urls import path
from . import views


app_name = 'groups'
urlpatterns = [
    path('<int:id>/', views.GroupDetail.as_view(), name='group'),
    path('<int:id>/create-post/', views.GroupPostCreate.as_view(), name='create_post'),
    path('<int:id>/update/', views.GroupUpdate.as_view(), name='update'),
    path('ajax/handle-join/<int:id>/', views.handle_join, name='handle_join'),
    path('create/', views.GroupCreate.as_view(), name='create'),
]