import tempfile
from typing_extensions import ParamSpecArgs

from django.http.response import Http404, HttpResponse, HttpResponseNotFound
from libraryshop.forms import CreateCollectionForm
from libraryshop.inc.db_functions import book_as_zip, user_owns_book, user_owns_chapter, user_purchase_book, user_purchase_chapt
from libraryshop.models import BookCollectionMapping, BookSection
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import InvalidQuery
from libraryshop.models import Collection, UserOwnBook
import datetime
from django.contrib import auth
from django.contrib.auth import logout, models
from django.contrib.auth import logout
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.edit import FormView
# user_own_book, user_purchase_book, get_books_in_collection
# from libraryshop.inc.db_functions import *
# from libraryshop.inc.db_functions import user_own_book
from libraryshop.models import Book
from django.core.exceptions import ObjectDoesNotExist
# from csci4830.libraryshop.models import BookSection

##############################
######## Class Views #########
##############################


class SearchFormView(FormView):
    from libraryshop.forms import SearchBookForm
    template_name = 'search.html'
    form_class = SearchBookForm
    success_url = 'results'


class CreateCollectionFormView(FormView):
    from libraryshop.forms import CreateCollectionForm
    template_name = 'addcollection.html'
    form_class = CreateCollectionForm


##############################
####### Function Views #######
##############################

def index(request):
    """This is the function that is executed when the root (/) url is called.

    It is called in urls.py (in the csci4830 controller folder, the last one)
    """

    try:
        book = Book.objects.latest('date_added_db') or None
    except:
        book = None

    try:
        collection = Collection.objects.latest('date_added_db')
    except:
        collection = None

    context = {
        'newest_book': book or None,
        'newest_collection': collection or None
    }

    return render(request, "index.html", context)


def collection(request, collection_id):
    errors = []
    collection = None
    books = []

    try:
        collection = Collection.objects.get(id=collection_id)
    except:
        collection = None

    book_mapping = BookCollectionMapping.objects.filter(
        collection_id=collection.id)
    for i in book_mapping:
        books.append(i.book_id)

    context = {
        'errors': errors,
        'collection': collection,
        'owner': collection.user_id,
        'results': books
    }
    return render(request, 'collection.html', context)
    pass


@login_required
def mycollections(request):
    errors = []
    try:
        collections = Collection.objects.filter(user_id=request.user)
    except:
        collections = None

    context = {
        'errors': errors,
        'collections': collections
    }
    return render(request, 'mycollections.html', context)


@login_required
def purchase(request, book_id):
    errors = []
    try:
        book: Book = Book.objects.get(id=book_id)
    except:
        book = None

    if book and not errors:
        try:
            new_purchase = user_purchase_book(request.user, book)
        except AlreadyRegistered:
            errors += [
                'You already own this book. Click <a href="' + '/downloads/' + str(book.id) + '">here</a> to read it!']
        except InvalidQuery:
            errors += ['Something happened with the query!']
        except Exception as e:
            errors += [str(e.__class__) + 'error']

    context = {
        'errors': errors,
        'book': book
    }

    return render(request, "purchase.html", context)


@login_required
def purchase_chapter(request):
    chapter_id = request.GET.get('chapter_selection', None)
    errors = []
    chapter = BookSection.objects.none
    try:
        chapter: BookSection = BookSection.objects.get(id=chapter_id)
        book = chapter.book_id
    except:
        errors.append("Chapter does not exist!")
        chapter = None

    if chapter and not errors:
        try:
            new_purchase = user_purchase_chapt(request.user, chapter)
            print('abab', book)
        except AlreadyRegistered:
            errors += [
                'You already own this chapter. Click <a href="' + '/download_chapter/' + str(chapter.id) + '">here</a> to read it!']
        except InvalidQuery:
            errors += ['Something happened with the query!']

    context = {
        'errors': errors,
        'chapter': chapter,
        'book': book
    }

    return render(request, "purchase_chapter.html", context)


def submitcollection(request):
    errors = []
    name = request.POST.get('name')
    books = request.POST.get('book_choices')
    form = CreateCollectionForm(request.POST)
    collection = Collection.objects.none
    if form.is_valid():
        ids = form.cleaned_data['book_choices']
        collection = Collection(name=name, user_id=request.user)
        try:
            collection.save()
        except:
            errors.append('Unable to create collection!')

        for i in ids:
            collection_mapping = BookCollectionMapping(
                book_id=i, collection_id=collection)
            try:
                collection_mapping.save()
            except Exception as e:
                errors.append(
                    'Unable to insert books into collection, error: ' + e)
                collection.delete()
                break

    context = {
        'errors': errors,
    }
    return render(request, 'submitcollection.html', context)


def buybook(request, book_id):

    errors = []
    user_own = False
    try:
        book: Book = Book.objects.get(id=book_id)
    except:
        book = None
        errors += ['Book does not exist!']

    if (book != None):
        user_own = user_owns_book(request.user, book)

    context = {
        'errors': errors,
        'book': book,
        'book_purchased': user_own
    }
    return render(request, "buybook.html", context)


def mybooks(request):
    owned_books = UserOwnBook.objects.filter(user_id=request.user.id)

    books = []
    for ownership in owned_books:
        books += [ownership.book_id]

    context = {
        'results': books,
        'owned_books': books
    }
    return render(request, "results.html", context)


def book(request, book_id: int):

    errors = ''

    book = None
    try:
        book = Book.objects.get(id=book_id)
    except:
        errors += '<p>Book does not exist.</p>'
        pass

    chapters = BookSection.objects.filter(book_id=book_id)
    context = {
        'book': book,
        'errors': errors,
        'user_owns_book': user_owns_book(request.user, book),
        'chapters': chapters
    }

    return render(request, "book.html", context)


def download(request, book_id: int, chapter_id: int):
    import os.path

    pass


def download(request, book_id: int):
    pass


def download_chapter(request, chapter_id: int):
    import os.path
    from csci4830.settings import MEDIA_ROOT

    try:
        chapter = BookSection.objects.get(id=chapter_id)
        book = Book.objects.get(id=chapter.book_id.id)
        if not user_owns_book(request.user, book) and not user_owns_chapter(request.user, chapter):
            return HttpResponseNotFound("You do not own this book. Out, out!")
    except:
        chapter = None
        book = None

    if book == None or chapter == None or chapter.file == None:
        return HttpResponseNotFound("Chapter does not exist.")

    fullpath = MEDIA_ROOT + str(chapter.file)
    try:
        if os.path.exists(fullpath):
            with open(fullpath, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(
                    book.title + ' - ' + book.author.firstname + ' ' + book.author.lastname + '.' + str(file.name).split('.')[-1])
            return response
    except Exception as e:
        return HttpResponseNotFound(e)

    return HttpResponseNotFound("Man")


def download(request, book_id: int):
    import os.path

    try:
        book = Book.objects.get(id=book_id)
        if not user_owns_book(request.user, book):
            return HttpResponseNotFound("You do not own this book. Out, out!")
        chapters = BookSection.objects.filter(book_id=book)
    except:
        book = None
        chapters = None

    if book == None:
        return HttpResponseNotFound("Book does not exist.")
    if chapters == None:
        return HttpResponseNotFound("Book does not contain chapters, please notify the administrator(s).")

    zipfile = book_as_zip(book)

    try:
        if os.path.exists(zipfile.name):
            with open(zipfile.name, 'rb') as file:
                print('fi', file)
                response = HttpResponse(
                    file.read(), content_type="application/zip")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(
                    book.title + ' - ' + book.author.firstname + ' ' + book.author.lastname + '.zip')
        return response
    finally:
        os.remove(zipfile.name)

    return Http404


def results(request):

    sb_year = sb_month = sb_day = None
    title = request.GET.get('title') or None  # Set to none if blank string
    author = request.GET.get('author') or None
    isbn = request.GET.get('isbn') or None
    genre = request.GET.get('genre') or None
    sb = request.GET.get('search_date_before') or None
    if (sb != None):
        sb = sb.split('-')
        if (len(sb) == 3):
            try:
                sb_year = int(sb[0])
                sb_month = int(sb[1])
                sb_day = int(sb[2])
            except:  # Error parsing values, throw 'em all out.
                sb_year = None
                sb_month = None
                sb_day = None

    sa = request.GET.get('search_after')

    results: QuerySet = Book.objects.all()

    if title != None:
        results = results.filter(title__icontains=title)
    if author != None:
        results = results.filter(author__exact=author)
    if (sb_year and sb_month and sb_day):
        print(sb_year, sb_month, sb_day)
        print(sb)
        results = results.filter(
            publication_date__lt=datetime.date(sb_year, sb_month, sb_day))
    if (isbn):
        results = results.filter(isbn__exact=isbn)
    if (genre):
        results = results.filter(genre__exact=genre)

    already_owned = {}
    for book in results:
        if user_owns_book(request.user, book):
            already_owned[book] = True

    context = {
        'results': results,
        'owned_books': already_owned
    }

    return render(request, "results.html", context)


"""
def results(request):
    from libraryshop.forms import SearchBookForm
    from libraryshop.inc.html_functions import print_book_result
    # Initialize

    hadQuery = False
    form = SearchBookForm()
    context = {
        'form': form,
        'hadQuery': False
    }
    # Search for submitted POST queries
    if request.method != 'POST':
        return render(request, "search.html", context)
    print("test")

    title = request.POST['title']  # String
    author = request.POST['author']  # Integer (id)
    isbn = request.POST['ISBN']  # String
    genre = request.POST['genre']  # Enumeration (string)
    # Integer (1 to 12)

    date_before = str(request.POST['search_date_before']).split('-')
    # if not date_before == ['']:
    date_after = str(request.POST['search_date_after'].split('-'))
    if not date_after == ['']:
        date_after_year = date_after[0]
        date_after_month = date_after[1]
        date_after_day = date_after[2]

    from libraryshop.models import Book
    from django.db.models import Q  # Trust the plan!
    import datetime

    results = Book.objects.all()

    if (title != "" and title != None):
        hadQuery = True
        results = results.filter(title__icontains=title)
    if (author):
        hadQuery = True
        results = results.filter(author__exact=author)
    if (isbn):
        hadQuery = True
        results = results.filter(isbn__icontains=isbn)
    if (genre):
        hadQuery = True
        results = results.filter(genre__exact=genre)
    if (len(date_before) == 3):
        date_before_year = int(date_before[0])
        date_before_month = int(date_before[1])
        date_before_day = int(date_before[2])
        if (date_before_year):
            if (date_before_month and date_before_month >= 1 and date_before_month <= 12):
                if (date_before_day and date_before_day >= 1 and date_before_day <= 31):
                    hadQuery = True
                    results = results.filter(publication_date__lt=datetime.date(
                        date_before_year, date_before_month, date_before_day))  # year/month/day
    if (len(date_after) == 3):
        date_after_year = int(date_after[0])
        date_after_month = int(date_after[1])
        date_after_day = int(date_after[2])
        if (date_after_year):
            if (date_after_month and date_after_month >= 1 and date_after_month <= 12):
                if (date_after_day and date_after_day >= 1 and date_after_day <= 31):
                    hadQuery = True
                    results = results.filter(publication_date__lt=datetime.date(
                        date_after_year, date_after_month, date_after_day))  # year/month/day

    context['hadQuery'] = hadQuery

    if hadQuery == False:
        return render(request, "search.html", context)

    print_book_result(results)

    return render(request, "search.html", context)
"""


def browse(request):
    pass

######


def login(request):
    from libraryshop.models import User
    from django.contrib.auth import authenticate, login

    login_status_mesg = ''
    postUsername = request.POST.get('username')
    postPassword = request.POST.get('password')
    session_user = authenticate(
        request, username=postUsername, password=postPassword)

    if User.objects.filter(username=postUsername).count() == 0:
        login_status_mesg += 'User does not exist!'
    elif session_user == None:
        login_status_mesg += 'Invalid username and password combination!'
    # else:
        # login_status_mesg += 'Invalid username and password combination!'

    print(login_status_mesg)
    from libraryshop.forms import LoginForm

    context = {
        'login_form': LoginForm(),
        'content_site': 'login.html',
        'login_status_mesg': login_status_mesg
    }
    return render(request, "registration/login.html", context)


def logout_view(request):
    logout(request)
    pass
