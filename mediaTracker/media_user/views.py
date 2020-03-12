from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import DetailView
from .models import MediaUser

class UserDetailView(DetailView):
    model = MediaUser
    template_name = 'user_detail.html'
    context_object_name = 'media_user'
    obj = super().get_object()
    return obj
