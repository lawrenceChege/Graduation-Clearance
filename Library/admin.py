from django.contrib import admin
from Library.models import Author, Book, BoorowedBook, Category, Publisher

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	"""
		Category Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created',)
	list_display = (
		'name', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'status__name')


    # Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	"""
		Author Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created',)
	list_display = (
		'name', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'status__name')

    # Register your models here.
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	"""
		Publisher Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created',)
	list_display = (
		'name', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'status__name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	"""
		Book Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'author', 'publisher')
	list_display = (
		'name', 'author', 'publisher', 'year_published', 'synopsis', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'author__name', 'publisher__name','status__name')


@admin.register(BoorowedBook)
class BoorowedBookAdmin(admin.ModelAdmin):
	"""
		BoorowedBook Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'student')
	list_display = (
		'student', 'book', 'borrowed_time', 'returned_time', 'due_date', 'penalty', 'status', 'date_modified', 'date_created')
	search_fields = ('book__name', 'student__first_name', 'student__first_name','status__name')