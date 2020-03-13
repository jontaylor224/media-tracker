from django import forms

class ISBNSearch(forms.Form):
    ISBN = forms.CharField(max_length=13)