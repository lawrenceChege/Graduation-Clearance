from django.db import models
from Finance.models import Fee

from system_users.models import SUser

from base.models import BaseModel, GenericBaseModel, State

class Category(GenericBaseModel):
    """
	Defines the different categories: history, fiction, mathematics
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.name, self.status)


class Author(GenericBaseModel):
    """
	Defines the Author
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.name, self.status)

class Publisher(GenericBaseModel):
    """
	Defines the publisher
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.name, self.status)

class Book(GenericBaseModel):
    """
    Defines the book
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    year_published = models.TextField(max_length=4, blank=True, null=True)
    synopsis = models.TextField(max_length=500, blank=True, null=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.name, self.author , self.publisher, self.year_published , self.status)


class BoorowedBook(BaseModel):
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_time = models.DateTimeField(auto_now=True)
    returned_time = models.DateTimeField(auto_now=True)
    due_date = models.DateField(auto_now_add=True)
    penalty = models.ForeignKey(Fee, on_delete=models.CASCADE)
    status = models.ForeignKey(State, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s %s %s %s %s' % (self.student, self.book, self.borrowed_time, self.due_date, self.status)

    

