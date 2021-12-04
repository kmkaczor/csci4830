from django.db.models.query_utils import InvalidQuery
from libraryshop.models import Book, BookSection, BookCollectionMapping, Collection, BookCollectionMapping, UserOwnBook, UserOwnBookSection
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from csci4830.settings import MEDIA_ROOT
from os.path import basename

from django.contrib.admin.sites import AlreadyRegistered
# https://stackoverflow.com/questions/34249632/how-to-serve-a-created-tempfile-in-django


def book_as_zip(book):
    was_chapter = False
    from zipfile import ZipFile
    from tempfile import NamedTemporaryFile
    try:
        chapters = BookSection.objects.filter(book_id=book)
    except:
        chapters = None

    with NamedTemporaryFile(delete=False) as tmp_zip:
        with ZipFile(tmp_zip, 'w') as zip:
            for chapter in chapters:
                was_chapter = True
                chapter_path = MEDIA_ROOT + str(chapter.file)
                zip.write(chapter_path, basename(
                    # 'chapter ' + str(chapter.chapter_num)) + '.' + chapter_path.split('.')[-1])
                    str(chapter.chapter_num)) + '. ' + chapter.chapter_title + '.' + chapter_path.split('.')[-1])
        return tmp_zip
    return None


def get_books_in_collection(collection: Collection):
    bookmap = BookCollectionMapping.objects.filter(collection_id=collection.id)


def user_owns_book(user, book):
    if book == None or user == None:
        return False

    user_own = UserOwnBook.objects.none

    try:
        user_own = UserOwnBook.objects.get(user_id=user.id, book_id=book.id)
    except ObjectDoesNotExist:
        return False

    if user_own:
        return True

    return False


def user_owns_chapter(user, chapter: BookSection):
    if chapter == None or user == None:
        return False

    user_own = UserOwnBookSection.objects.none

    # If they own the book, they own the chapter.
    if user_owns_book(user, chapter.book_id):
        return True
    try:
        user_own = UserOwnBookSection.objects.get(
            user_id=user.id, book_section_id=chapter.id)
    except ObjectDoesNotExist:
        return False

    if user_own:
        return True

    return False


def user_purchase_chapt(user, chapter: BookSection):
    if user == None or chapter == None:
        return InvalidQuery
    if user_owns_chapter(user, chapter):
        raise AlreadyRegistered

    new_purchase = UserOwnBookSection(user_id=user, book_section_id=chapter)
    new_purchase.save()
    if (new_purchase == None):
        raise InvalidQuery

    return new_purchase


def user_purchase_book(user, book):
    if user == None or book == None:
        return InvalidQuery

    if user_owns_book(user, book):
        raise AlreadyRegistered

    new_purchase = UserOwnBook(user_id=user, book_id=book)
    new_purchase.save()
    if (new_purchase == None):
        raise InvalidQuery

    return new_purchase


"""

def user_owns_book(user: User, book: Book):
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
"""


#setattr(User, "has_book", has_book)
