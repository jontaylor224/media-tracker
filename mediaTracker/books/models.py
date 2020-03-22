from django.db import models
from mediaTracker.media_user.models import MediaUser


class Book(models.Model):
    ISBN = models.CharField(max_length=13, blank=True, null=True)
    title = models.CharField(max_length=120, blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    publisher = models.CharField(max_length=100, blank=False, null=True)
    pubDate = models.DateField(blank=True, null=True)
    coverThumbURL = models.URLField(blank=True, null=True)
    description = models.TextField('Description', null=True, blank=True)
    collection = models.ForeignKey(
        MediaUser, related_name='collection', blank=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
