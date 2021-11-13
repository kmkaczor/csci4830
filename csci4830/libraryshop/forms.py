from django import forms
from django.contrib.auth.models import User
from django.db.models.fields import DateField
from libraryshop.models import Book


class SearchBookForm(forms.ModelForm):
    search_date_before = forms.DateField(widget=forms.SelectDateWidget)
    search_date_after = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'ISBN',
            'genre',
            # 'publication_date'
        ]
    pass


"""
class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

"""
