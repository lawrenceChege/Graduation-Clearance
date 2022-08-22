from pydoc import synopsis
from tkinter.tix import Balloon
from django.db import models

from base.models import BaseModel, GenericBaseModel, State

class Category(GenericBaseModel):
    """
	Defines the different categories: history, fiction, mathematics
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class Author(GenericBaseModel):
    """
	Defines the Author
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class Publisher(GenericBaseModel):
    """
	Defines the publisher
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class Book(GenericBaseModel):
    """
    Defines the book
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    year_published = models.TextField(max_length=4, blank=True, null=True)
    synopsis = models.TextField(max_length=500, blank=True, null=True)


class BoorowedBook(BaseModel):
    

