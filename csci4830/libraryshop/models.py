from django.db import models

from django.db.models.fields import CharField, IntegerField


class Author(models.Model):
    firstname = CharField(max_length=60)
    lastname = CharField(max_length=60)


class Book(models.Model):
    # We use a foreign key as Author is its own table
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = CharField(max_length=250)
    isbn = IntegerField(13)  # Might change this to cha

    # Great a list of genre choices
    ENUM_GENRES = (
        "Horror", "Romance", "Non-fiction", "Fantasy", "Science Fiction",
        "Mystery", "Historial Fiction", "Children", "Autobiography", "History",
        "Cookbook"
    )
    genre = models.CharField(max_length=max(
        ENUM_GENRES, key=len), choices=ENUM_GENRES)


# Chapters, Individual Recipes, etc.


class BookSection(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    chapter_num = IntegerField(13)

    # Create your models here.
