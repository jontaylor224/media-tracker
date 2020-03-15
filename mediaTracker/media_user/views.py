from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import DetailView
from .models import MediaUser
from .forms import UserForm

class UserDetailView(DetailView):
    model = MediaUser
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def add_user(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_data = user_form.cleaned_data
                username = user_data.get("username"),
                password1 = user_data.get("password1")
                password2 = user_data.get("password2")
                if password1 == password2:
                    new_user = User.objects.create_user(
                        username=username,
                        password=password1
                    )
                    new_media_user = MediaUser.objects.create(
                        user=new_user,
                        email=user_data.get("email")
                    )
                    new_media_user.save()
                return HttpResponseRedirect('/')
        else:
            user_form = UserForm()
        return render(request, 'add_user.html', {'form':user_form})
