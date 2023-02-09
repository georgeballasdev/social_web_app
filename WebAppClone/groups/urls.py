from django.urls import path
from . import views


app_name = 'groups'
urlpatterns = [
    path('<int:id>/', views.GroupDetail.as_view(), name='group'),
    path('<int:id>/create-post/', views.GroupPostCreate.as_view(), name='create_post'),
    path('<int:id>/update/', views.GroupUpdate.as_view(), name='update'),
    path('<int:id>/manage/', views.manage_members, name='manage'),
    path('create/', views.GroupCreate.as_view(), name='create'),
    path('ajax/handle-membership/<int:id>/', views.handle_membership, name='handle_membership'),
    path('ajax/handle-member/<int:id>/', views.handle_member, name='handle_member'),
]