from django import forms
from .models import MediaUser


class UserForm(forms.Form):
    username = forms.CharField(max_length=25)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=25)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=25)
    email = forms.EmailField()
