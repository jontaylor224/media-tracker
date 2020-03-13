from django.db import models
from mediaTracker.media_user.models import MediaUser

class Book(models.Model):
    ISBN = models.CharField(max_length=13, blank=True, null=True)
    title = models.CharField(max_length=120, blank=False, null=False)
    author1 = models.CharField(max_length=100, blank=False, null=False)
    author2 = models.CharField(max_length=100, blank=True, null=True)
    pubDate = models.DateField(blank=True, null=True)
    coverThumbURL = models.URLField(blank=True, null=True)
    isInPrint = models.BooleanField(default=True)
    seriesName = models.CharField(max_length=200, blank=True, null=True)
    seriesNum = models.IntegerField(blank=True, null=True)
    description = models.TextField('Description', null=True, blank=True)
    collection = models.ForeignKey(MediaUser, related_name='collection', blank=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

