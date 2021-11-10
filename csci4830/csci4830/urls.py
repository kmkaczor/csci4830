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

#       Browser path           Path from project root (directory with manage.py)
#       ''              =    "/"
#       'book'          =    "/book"
#       'admin'         =    "/admin"

urlpatterns = [
    path('', views.index, name="index"),  # To access in browser: /
    path('book', views.book, name="book"),  # To access in browser /book
    path('search', views.search, name="search"),  # /search
    path('browse', views.browse, name="browse"),  # /search
    path('admin', admin.site.urls, name="admin")  # To access in browser /book

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Allow static files for developemnt mode
