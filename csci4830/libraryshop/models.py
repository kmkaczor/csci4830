from django.db import models
from django.db.models.deletion import DO_NOTHING

from django.db.models.fields import CharField, EmailField, IntegerField


class UserAccount(models.Model):
    firstname = CharField(max_length=60)
    lastname = CharField(max_length=60)
    # Hashed, django probably has a function to automate this
    username = CharField(max_length=60)

    email = EmailField(max_length=100)
    password = CharField(max_length=100)

    def __sttr__(self):
        return self.username


class Author(models.Model):
    firstname = CharField(max_length=60)
    lastname = CharField(max_length=60)


# The Book table
class Book(models.Model):
    # We use a foreign key as Author is its own table
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = CharField(max_length=250)
    isbn = IntegerField(13)  # Might change this to cha

    # Great a list of genre choices
    ENUM_GENRES = (
        ('HORROR', 'Horror'),
        ('ROMANC', 'Romance'),
        ('NONFIC', 'Non-fiction'),
        ('FANTAS', 'Fantasy'),
        ('SCIFIC', 'Science Fiction'),
        ('MYSTER', 'Mystery'),
        ('HSTFIC', 'Historial Fiction'),
        ('CHLDRN', 'Childrens'),
        ('ATOBIO', 'Autobiography'),
        ('HISTRY', 'History'),
        ('COOKBK', 'Cookbook')
    )
    genre = models.CharField(max_length=6, choices=ENUM_GENRES)

# Chapters, Individual Recipes, etc.


class BookSection(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    chapter_num = IntegerField(13, unique=True)  # Chapter numbers are unique
    file = CharField(max_length=500)  # Absolute path to file location

# Mapping user and books -- user owns what books?
# user_id and book_id should not have duplicates together


class UserOwnership:
    user_id = models.ForeignKey(UserAccount, on_delete=models.DO_NOTHING)
    book_id = models.ForeignKey(BookSection, on_delete=models.DO_NOTHING)
# The "Author" table
