from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import TemplateView

from ..books.models import Book
from .forms import LoginForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'mediauser'):
            context['num_of_books'] = \
                self.request.user.mediauser.collection.count()
        else:
            context['num_of_books'] = 0
        return context


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage'))
            )
    form = LoginForm
    return render(request, 'login_form.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
