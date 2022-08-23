from django.urls import path

from . import views

urlpatterns = [
    # ex: /store/
    path('', views.view_all_borrowed_books, name='all borrowed books'),
    path('borrowed_book/add', views.add_borrowed_book, name='new borrowed_book'),
    path('borrowed_book/view', views.view_borrowed_book, name='show borrowed_book'),
    path('borrowed_book/update', views.update_borrowed_book, name='update borrowed_book'),
    path('category/all', views.view_all_categories, name='all categories'),
    path('category/add', views.add_category, name='new category'),
    path('category/view', views.view_category, name='show category'),
    path('category/update', views.update_category, name='update category'),
    path('author/all', views.view_all_authors, name='all authors'),
    path('author/add', views.add_author, name='new author'),
    path('author/view', views.view_author, name='show author'),
    path('author/update', views.update_author, name='update author'),
    path('publisher/all', views.view_all_publishers, name='all publishers'),
    path('publisher/add', views.add_publisher, name='new publisher'),
    path('publisher/view', views.view_publisher, name='show publisher'),
    path('publisher/update', views.update_publisher, name='update publisher'),
    path('book/all', views.view_all_books, name='all books'),
    path('book/add', views.add_book, name='new book'),
    path('book/view', views.view_book, name='show book'),
    path('book/update', views.update_book, name='update book'),
]