from enum import unique
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import CharField, DateField, DateTimeField, DecimalField, EmailField, FloatField, IntegerField, PositiveIntegerField, TextField
from django.db import models
from django.db.models.deletion import DO_NOTHING
from abc import ABC
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile, FileField, ImageField, ImageFieldFile
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import InvalidQuery
from django.forms.widgets import ClearableFileInput


"""
def has_book(user, book):
    if book == None:
        return False

    try:
        user_own = UserOwnBook.objects.get(user_id=user.id, book_id=book.id)
    except ObjectDoesNotExist:
        return False
    return True


setattr(User, "has_book", has_book)


def buybook(user, book):
    if book == None:
        raise FileNotFoundError  # Whatever, I'm doing this "team" assignment in a hurry

    if user.has_book(book):
        raise FileExistsError

    new_ownership = UserOwnBook(user_id=user.id, book_id=book.id)
    new_ownership.save()

    return new_ownership


setattr(User, "buybook", buybook)
"""


class UserProfile(models.Model):
    """This hold user options that would fit within the User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Author(models.Model):
    """Table of authors.
    """
    firstname = CharField(max_length=60, null=True, blank=True)
    lastname = CharField(max_length=60)

    def __str__(self):
        return (self.firstname or '') + ' ' + (self.lastname or '')


class Book(models.Model):
    def cover_image_path(book, filename):
        extension = str(filename).split(sep='.')[-1]
        return 'book/{0}/img/cover.{1}'.format(book.pk, extension)

    # Blank is true. This disables fields in forms being labeled as "required" which is unwanted for search
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=False)
    title = CharField(max_length=250, null=False)
    publication_date = DateField(null=True, blank=True)
    date_added_db = DateTimeField(auto_created=True, auto_now_add=True)
    date_edit_db = DateTimeField(auto_created=True, auto_now=True)
    description = TextField(null=True, blank=True)
    isbn = CharField(max_length=14, name="ISBN", null=True, blank=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cover_image = ImageField(upload_to=cover_image_path,
                             max_length=250, blank=True, null=True)

    # Workaround for saved images being saved according to ID before ID was assigned, thus creating None directory.

    def save(self, *args, **kwargs):
        """Overloaded save method to prevent saving cover image before the id is generated.
        """
        if self.pk == None:
            img_tmp = self.cover_image
            self.cover_image = None
            # Ensure that the object exists before saving the image, as the id isn't generated yet.
            super().save(*args, **kwargs)
            self.cover_image = img_tmp

        return super().save(*args, **kwargs)

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
        ('PHILOS', 'Philosophy'),
        ('HISTRY', 'History'),
        ('COOKBK', 'Cookbook')
    )
    genre = models.CharField(max_length=6, choices=ENUM_GENRES, blank=True)

    def chapters(self):
        BookSection

    def __str__(self):
        return self.title + " by " + str(self.author)


class Collection(models.Model):
    name = CharField(max_length=80, null=False)
    user_id = ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    date_added_db = DateField(auto_created=True, auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=[   # Applies a constraint to UserOwnership to ensure the combination of user_id and book_id is unique
                'name', 'user_id'
            ], name='constraint_collection_uniq_title_per_user')
        ]


class BookCollectionMapping(models.Model):
    book_id = ForeignKey(Book, on_delete=DO_NOTHING, null=False)
    collection_id = ForeignKey(Collection, on_delete=DO_NOTHING, null=False)


class BookSection(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=False)
    chapter_title = CharField(max_length=1000, null=True)
    # Chapter numbers are unique
    chapter_num = PositiveIntegerField('Chapter number')
    price = DecimalField(null=True, max_digits=6, decimal_places=2)

    def book_section_path(section, filename):
        extension = str(filename).split(sep='.')[-1]
        return 'book/{0}/section/chapter{1}.{2}'.format(section.book_id.id, section.chapter_num, extension)

    file = FileField(upload_to=book_section_path, max_length=250,
                     unique=True)  # Absolute path to file location

    class Meta:
        constraints = [
            UniqueConstraint(fields=[   # Applies a constraint to UserOwnership to ensure the combination of user_id and book_id is unique
                'book_id', 'chapter_num'
            ], name='constraint_book_chapter')
        ]

    def __str__(self):
        return self.chapter_title

# Mapping user and books -- user owns what books?
# user_id and book_id should not have duplicates together


class UserOwnBookSection(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, unique=False)
    book_section_id = models.ForeignKey(
        BookSection, on_delete=models.DO_NOTHING, unique=False)

    # The below line doesn't appear to work correctly on MySQL.
    class Meta:
        unique_together = [['user_id', 'book_section_id']]


class UserOwnBook(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, unique=False)
    book_id = models.ForeignKey(
        Book, on_delete=models.DO_NOTHING, unique=False)

    # The below line doesn't appear to work correctly on MySQL.
    class Meta:
        unique_together = [['user_id', 'book_id']]

    # constraints = [

    #    UniqueConstraint(fields=[
    #        'user_id', 'book_id'
    #    ], name='constraint_book_owner')
    # ]
