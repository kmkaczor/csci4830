from django.contrib.admin.sites import AlreadyRegistered
from django.db.models.query_utils import InvalidQuery
from libraryshop.models import Book, BookCollectionMapping, Collection, BookCollectionMapping, UserOwnBook
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def get_books_in_collection(collection: Collection):
    bookmap = BookCollectionMapping.objects.filter(collection_id=collection.id)
    return None


