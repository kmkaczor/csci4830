from django.forms.widgets import ClearableFileInput
from libraryshop.models import BookSection
from libraryshop.models import Author
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import DateField
from libraryshop.models import Book


# Use calendar for search forms
# https://stackoverflow.com/a/35968816
class DateInput(forms.DateInput):
    input_type = 'date'


class CreateCollectionForm(forms.Form):
    name = forms.CharField(required=True)
    book_choices = forms.ModelMultipleChoiceField(
        queryset=Book.objects.all())  # This is absolutely not scalable!


class SearchBookForm(forms.ModelForm):
    title = forms.CharField(required=False)
    author = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(), required=False)
    search_date_before = forms.DateField(widget=DateInput(), required=False)
    search_date_after = forms.DateField(widget=DateInput(), required=False)
    success_url = 'result'

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'ISBN',
            'genre',
            # 'publication_date'
        ]
        widgets = {
            # 'publication_date': DateInput()
        }

    pass

    def clean(self):
        super(SearchBookForm, self)

        before_date = self.cleaned_data.get('search_date_before')

        if self.cleaned_data.get('title') == 'hello':
            self.title = 'the'

        if (before_date != None):
            before_year = before_date.year
            before_month = before_date.month
            before_day = before_date.day
            print(before_day)

        return self.cleaned_data


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class CollectionForm(forms.ModelForm):
    chapters = forms.FileField(
        widget=ClearableFileInput(attrs={'multiple': True}))
