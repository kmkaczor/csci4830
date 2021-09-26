from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # render("Hello, world. Can you see me?", "")
    return HttpResponse("Hello world. Can you see this?")
# Create your views here.
