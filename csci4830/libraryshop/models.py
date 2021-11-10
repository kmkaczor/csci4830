from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import CharField, EmailField, IntegerField, TextField
from django.db import models
from django.db.models.deletion import DO_NOTHING
from abc import ABC
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile, FileField, ImageField, ImageFieldFile


# We are extending Django's built-in user account. See django.contrib.auth.models for the good stuff
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Author(models.Model):
    firstname = CharField(max_length=60)
    lastname = CharField(max_length=60)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

# The Book table


class Book(models.Model):
    def cover_image_path(book, filename):
        extension = str(filename).split(sep='.')[-1]
        return 'book/{0}/cover.{1}'.format(book.pk, extension)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = CharField(max_length=250)
    description = TextField(null=True)
    isbn = CharField(max_length=14, name="ISBN", null=True)
    cover_image = ImageField(upload_to=cover_image_path,
                             max_length=250, null=True, unique=True)

    # Workaround for saved images being saved according to ID before ID was assigned, thus creating None directory.

    def save(self, *args, **kwargs):
        if self.pk == None:
            img_tmp = self.cover_image
            self.cover_image = None
            super().save(*args, **kwargs)
            self.cover_image = img_tmp

        return super().save(*args, **kwargs)

    def get_cover_image(self):
        pass
        # self.cover_image.
        return self.cover_image

    def __str__(self):
        return self.title + " by " + str(self.author)

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


class BookSection(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    chapter_title = CharField(max_length=1000, null=True)
    chapter_num = IntegerField(13, unique=True)  # Chapter numbers are unique
    file = CharField(max_length=500)  # Absolute path to file location

    def __str__(self):
        return self.chapter_title

# Mapping user and books -- user owns what books?
# user_id and book_id should not have duplicates together


# Abstract class for owning chapters or entire books
class UserOwnership(models.Model):
    user_id = models.OneToOneField(UserAccount, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class UserOwnChapter(UserOwnership):
    chapter_id = models.OneToOneField(BookSection, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(fields=[   # Applies a constraint to UserOwnership to ensure the combination of user_id and book_id is unique
                'user_id', 'chapter_id'
            ], name='constraint_chapter_owner')
        ]


class UserOwnBook(UserOwnership):
    book_id = models.OneToOneField(Book, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(fields=[   # Applies a constraint to UserOwnership to ensure the combination of user_id and book_id is unique
                'user_id', 'book_id'
            ], name='constraint_book_owner')
        ]

    # The "Author" table
