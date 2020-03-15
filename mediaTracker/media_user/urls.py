from django.urls import path
from .views import UserDetailView, add_user

urlpatterns = [
    path('users/<int:pk>', UserDetailView.as_view(), name='user_view'),
    path('add_user', add_user, name='add_user')
]