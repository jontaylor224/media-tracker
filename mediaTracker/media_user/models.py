from django.db import models
from django.contrib.auth.models import User
from mediaTracker.books.models import Book


class MediaUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(blank=True)
    collection = models.ManyToManyField(
        Book, related_name='collection', blank=True)

    def __str__(self):
        return self.user.username
