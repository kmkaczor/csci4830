from django import forms
from django.contrib.auth.models import User
from libraryshop.models import Book


class SearchBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'ISBN',
            'genre',
            'publication_date'
        ]
    # title = forms.charField(label="Title", max)
    #author = forms.charField(label="Author")
    # isbn
    pass


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']
