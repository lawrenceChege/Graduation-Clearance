from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.
def add_category(request):
    return HTTPResponse("category added")

def update_category(request):
    return HTTPResponse("category updated")

def view_category(request):
    return HTTPResponse("category")

def view_all_categories(request):
    return HTTPResponse("all categories")

def add_author(request):
    return HTTPResponse("author added")

def update_author(request):
    return HTTPResponse("author updated")

def view_author(request):
    return HTTPResponse("author")

def view_all_authors(request):
    return HTTPResponse("All authors")

def add_publisher(request):
    return HTTPResponse("publisher added")

def update_publisher(request):
    return HTTPResponse("publisher updated")

def view_publisher(request):
    return HTTPResponse("publisher")

def view_all_publishers(request):
    return HTTPResponse("All publishers")

def add_book(request):
    return HTTPResponse("book added")

def update_book(request):
    return HTTPResponse("book updated")

def view_book(request):
    return HTTPResponse("book")

def view_all_books(request):
    return HTTPResponse("All books")

def add_borrowed_book(request):
    return HTTPResponse("borrowed_book added")

def update_borrowed_book(request):
    return HTTPResponse("borrowed_book updated")

def view_borrowed_book(request):
    return HTTPResponse("borrowed_book")

def view_all_borrowed_books(request):
    return HTTPResponse("All borrowed_books")