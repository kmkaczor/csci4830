"""csci4830 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from libraryshop import views
from django.contrib.auth.decorators import login_required

#       Browser path           Path from project root (directory with manage.py)
#       ''              =    "/"
#       'book'          =    "/book"
#       'admin'         =    "/admin"

urlpatterns = [  # The name field is referenced in templates: see templates/navbar.html use the "url" template command
    path('', views.index, name="index"),  # To access in browser: /
    # To access in browser /book
    path('book/<int:book_id>/', views.book, name="book"),
    path('downloads/<int:book_id>', views.download, name="downloads"),
    path('results', views.results, name="results"),  # /results
    path('browse', views.results, name="browse"),  # /search with all results
    path('search', views.SearchFormView.as_view(), name="search"),  # /search
    path('buybook/<int:book_id>', views.buybook, name="buybook"),  # /search
    path('purchase/<int:book_id>', views.purchase, name="purchase"),  # /search
    path('addcollection', login_required(views.CreateCollectionFormView.as_view()),
         name="addcollection"),
    path('admin', admin.site.urls, name="admin"),  # To access in browser /book
    path('login', views.login, name="login"),  # To access in browser /book
    path('mybooks', views.mybooks, name='mybooks'),
    path('mycollections', views.mycollections, name='mycollections'),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Allow static files for developemnt mode
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
