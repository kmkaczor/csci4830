from libraryshop.models import Book, BookCollectionMapping, Collection, BookCollectionMapping, UserOwnBook
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def get_books_in_collection(collection: Collection):
    bookmap = BookCollectionMapping.objects.filter(collection_id=collection.id)


def user_own_book(user, book):
    try:
        user_own = UserOwnBook.objects.get(user_id=user.id, book_id=book.id)
    except ObjectDoesNotExist:
        return False
    return True


def has_book(user, book):
    if book == None:
        return False

    try:
        user_own = UserOwnBook.objects.get(user_id=user.id, book_id=book.id)
    except ObjectDoesNotExist:
        return False
    return True


setattr(User, "has_book", has_book)
