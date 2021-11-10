from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import CharField, DateField, EmailField, IntegerField, TextField
from django.db import models
from django.db.models.deletion import DO_NOTHING
from abc import ABC
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile, FileField, ImageField, ImageFieldFile


# We are extending Django's built-in user account. See django.contrib.auth.models for the good stuff
class UserAccount(models.Model):
    """An extended version of django's built-in user model.

    This may eventually be stripped out and replaced with the regular user model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Author(models.Model):
    """Table of authors.


    """
    firstname = CharField(max_length=60)
    lastname = CharField(max_length=60)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Book(models.Model):
    def cover_image_path(book, filename):
        extension = str(filename).split(sep='.')[-1]
        return 'book/{0}/cover.{1}'.format(book.pk, extension)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = CharField(max_length=250)
    publication_date = DateField(null=True)
    date_added_db = DateField(auto_created=True)
    date_edit_db = DateField(auto_created=True, auto_now_add=True)
    description = TextField(null=True)
    isbn = CharField(max_length=14, name="ISBN", null=True)
    cover_image = ImageField(upload_to=cover_image_path,
                             max_length=250, null=True, unique=True)

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
            ('HISTRY', 'History'),
            ('COOKBK', 'Cookbook')
        )
        genre = models.CharField(max_length=6, choices=ENUM_GENRES)

        def __str__(self):
            return self.title + " by " + str(self.author)


class BookSection(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=False)
    chapter_title = CharField(max_length=1000, null=True)
    chapter_num = IntegerField(13, unique=True)  # Chapter numbers are unique
    file = CharField(max_length=500)  # Absolute path to file location

    class Meta:
        constraints = [
            UniqueConstraint(fields=[   # Applies a constraint to UserOwnership to ensure the combination of user_id and book_id is unique
                'user_id', 'chapter_id'
            ], name='constraint_book_chapter')
        ]

    def __str__(self):
        return self.chapter_title

# Mapping user and books -- user owns what books?
# user_id and book_id should not have duplicates together


# Abstract class for owning chapters or entire books
class UserOwnership(models.Model):
    """Abstract base class for lookup tables on user owning chapters or books

    Thus inheritance looks like: models.Model -> UserOwnership -> UserOwnChapter or UserOwnBook
    """
    user_id = models.OneToOneField(UserAccount, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class UserOwnChapter(UserOwnership):
    chapter_id = models.OneToOneField(BookSection, on_delete=models.DO_NOTHING)

    def __str__(self):
        return BookSection(chapter_id=self.chapter_id) + " " + super(self)

    class Meta:
        constraints = [
            UniqueConstraint(fields=[
                'user_id', 'chapter_id'
            ], name='constraint_chapter_owner')
        ]


class UserOwnBook(UserOwnership):
    book_id = models.OneToOneField(Book, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(fields=[
                'user_id', 'book_id'
            ], name='constraint_book_owner')
        ]
