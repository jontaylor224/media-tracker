from django.urls import path
from .views import UserDetailView, add_user, all_users_view

urlpatterns = [
    path('users/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('add_user', add_user, name='add_user'),
    path('all_users', all_users_view, name='all_users')
]