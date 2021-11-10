from django.shortcuts import render

# from csci4830.libraryshop.models import BookSection


# Also look at urls.py
# Visit the very top directory (/)


def index(request):
    from libraryshop.models import Book
    """This is the function that is executed when the root (/) url is called.

    It is called in urls.py (in the csci4830 controlled folder, the last one)
    """
    varSetInViews = "Please check views.py to see the variable for this string."
    # In order this to work, we must have this allowed in urls.py

    for book in Book.objects.all():
        print(book.id)

    context = {
        "passedVariableFromRender":  varSetInViews,
        'pagetitle': "Index File",
    }

    return render(request, "skeleton.html", context)


def book(request):
    from libraryshop.models import Book
    # The following statements will print out out in "python3 manage.py runserver" terminal window
    # Listing all the genres in the book object, which is a tuple of two strings.
    allBooks = Book.ENUM_GENRES
  # Note how resultstring is initalized as a string?
    resultstr = '<ul>'

   # For loop going through every genre, wrapping string with unordered lists
    for book in allBooks:
        resultstr += "<li>" + book[1] + "</li>"
    resultstr += '</ul>'

    # Context variable. Note the pagetitle and passedVariableFromRender? You'll see them in the template files between braces: {{ pagetitle }}
    context = {
        'pagetitle': "Book page",
        # Note that HTML isn't escaped because |safe is mark in the template.
        'passedVariableFromRender': resultstr
    }

    # We are using the base template skeleton.html, which is in libraryshop/includes/templates
    return render(request, "skeleton.html", context)


def search(request):
    from libraryshop.forms import SearchBookForm
    form = SearchBookForm()

    context = {
        'passedVariableFromRender': form
    }
    return render(request, "skeleton.html", context)


def browse(request):

    pass
