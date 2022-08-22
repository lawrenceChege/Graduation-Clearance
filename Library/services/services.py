"""
	Services for models of library module
"""


from Library.models import Book, BoorowedBook, Publisher, Author, Category
from base.services.servicebase import ServiceBase


class CategoryService(ServiceBase):
	"""
		The service for handling CRUD events for the Category model
	"""
	manager = Category.objects


class AuthorService(ServiceBase):
	"""
		The service for handling CRUD events for the Author model
	"""
	manager = Author.objects


class PublisherService(ServiceBase):
	"""
		The service for handling CRUD events for the Publisher model
	"""
	manager = Publisher.objects


class BookService(ServiceBase):
	"""
		The service for handling CRUD events for the Book model
	"""
	manager = Book.objects


class BorrowedBookService(ServiceBase):
	"""
		The service for handling CRUD events for the BorrrowedBook model
	"""
	manager = BoorowedBook.objects
