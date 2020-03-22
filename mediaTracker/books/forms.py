from django import forms
from .models import Book


class ISBNSearch(forms.Form):
    ISBN = forms.CharField(max_length=13)


class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['ISBN', 'title', 'author',
                  'publisher', 'pubDate', 'description', 'collection']
