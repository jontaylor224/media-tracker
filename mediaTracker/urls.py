"""mediaTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from mediaTracker.authentication.urls import urlpatterns as auth_urls
from mediaTracker.books.urls import urlpatterns as book_urls
from mediaTracker.media_user.urls import urlpatterns as user_urls

from mediaTracker.books.models import Book
from mediaTracker.media_user.models import MediaUser

admin.site.register(MediaUser)
admin.site.register(Book)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += book_urls
urlpatterns += user_urls
urlpatterns += auth_urls

# FOR DEVELOPMENT ONLY, NOT SAFE FOR PRODUCTION
urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve)]
# staticfiles_urlpatterns()



# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)