from django.urls import path

from mediaTracker.authentication.views import (
    IndexView, login_view, logout_view)

urlpatterns = [
    path('', IndexView.as_view(), name='homepage'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
