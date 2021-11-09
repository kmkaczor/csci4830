from django.shortcuts import render

from libraryshop.models import *

#from csci4830.libraryshop.models import BookSection
from libraryshop.models import *


# Also look at urls.py
# Visit the very top directory (/)
def index(request):
    varSetInViews = "Please check views.py to see the variable for this string."
    # In order this to work, we must have this allowed in urls.py

    context = {
        "passedVariableFromRender":  varSetInViews,
        'pagetitle': "Index File",
    }

    return render(request, "skeleton.html", context)


# Visit the book directory (/book)
def book(request):
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
        'passedVariableFromRender': resultstr
    }

    # We are using the base template skeleton.html, which is in libraryshop/includes/templates
    return render(request, "skeleton.html", context)
