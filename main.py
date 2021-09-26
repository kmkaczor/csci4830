from django.db import models

class Book(models.Model):
    author_lastname = models.CharField(max_length=30)
    author_firstname = models.CharField(max_length=30)