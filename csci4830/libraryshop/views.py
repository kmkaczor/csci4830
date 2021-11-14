import datetime
from django.contrib.auth import logout
from django.contrib.auth import logout
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.edit import FormView
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
    template_name = ''

##############################
####### Function Views #######
##############################


def index(request):
    """This is the function that is executed when the root (/) url is called.

    It is called in urls.py (in the csci4830 controller folder, the last one)
    """
    varSetInViews = "Please check views.py to see the variable for this string."

    # The following line queries the database for all the book objects , then prints their ID numbers generated by django
    for book in Book.objects.all():
        print(book.id)

    # We pass this to render() in the return statement to give the template variable values to insert in the html
    context = {
        "passedVariableFromRender":  varSetInViews,
        'pagetitle': "Index File",
    }

    return render(request, "skeleton.html", context)


def book(request, book_id: int):
    errors = ''
    print(book_id)

    if (book_id == None):
        id = 0

    book: Book = Book.objects.none

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        errors += "Book does not exist."
        pass

    print(book)
    # print(book.cover_image_path())
    
    if 

    context = {
        'book': book,
        'errors': errors
    }

    # We are using the base template skeleton.html, which is in the templates folder
    return render(request, "book.html", context)


def results(request):

    if request.method != 'GET':
        pass

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
            finally:  # Error parsing values, throw 'em all out.
                sb_year = None
                sb_month = None
                sb_day = None

    sa = request.GET.get('search_after')

    results: QuerySet = Book.objects.all()

    if title != None:
        results = results.filter(title__icontains=title)
    if (sb_year and sb_month and sb_day):
        print(sb_year, sb_month, sb_day)
        print(sb)
        results = results.filter(
            publication_date__lt=datetime.date(sb_year, sb_month, sb_day))
    if (isbn):
        results = results.filter(isbn__exact=isbn)
    if (genre):
        results = results.filter(genre__exact=genre)

    context = {
        'results': results
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
    session_user = None

    if User.objects.filter(username=postUsername).count() == 0:
        login_status_mesg += 'User does not exist!'
    elif (session_user := authenticate(request, username=postUsername, password=postPassword)) == None:
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
