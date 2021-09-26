from django.db import models

class Author(models.Model):

class Book(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE) # We use a foreign key as Author is its own table
    author_firstname = models.CharField(max_length=30)