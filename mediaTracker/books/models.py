from django.db import models


class Book(models.Model):
    ISBN_13 = models.CharField(max_length=13, blank=True, null=True)
    ISBN_10 = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=120, blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    publisher = models.CharField(max_length=100, blank=False, null=True)
    pubDate = models.DateField(blank=True, null=True)
    coverThumbURL = models.URLField(blank=True, null=True)
    description = models.TextField('Description', null=True, blank=True)

    def __str__(self):
        return self.title
