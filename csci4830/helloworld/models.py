# main.py
# Korey Kaczor
# CSCI 4830 Hello World

from django.db import models
from django.db.models.fields import CharField, IntegerField


class Author(models.Model):
    firstname = CharField(max_length=60)
    lastname = CharField(max_length=60)


class Book(models.Model):
    # We use a foreign key as Author is its own table
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = CharField(max_length=250)
    isbn = IntegerField(13)  # Might change this to char
