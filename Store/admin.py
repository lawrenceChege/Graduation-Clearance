from django.contrib import admin

from Store.models import BorrowedGown, BorrowedGownPenalty, GraduationGown

# Register your models here.
@admin.register(GraduationGown)
class GraduationGownAdmin(admin.ModelAdmin):
	"""
		GraduationGown Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('purchasing_date', 'size', 'programme')
	list_display = (
		'purchasing_date', 'size', 'programme', 'fee', 'status', 'date_modified', 'date_created')
	search_fields = ('purchasing_date', 'size', 'programme', 'status__name')


    # Register your models here.
@admin.register(BorrowedGown)
class BorrowedGownAdmin(admin.ModelAdmin):
	"""
		BorrowedGown Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('borrow_date',)
	list_display = (
		'student', 'gown', 'borrow_date', 'return_date', 'penalty', 'balance', 'status', 'date_modified', 'date_created')
	search_fields = ('borrow_date', 'student__first_name', 'student__last_name', 'status__name')


    # Register your models here.
@admin.register(BorrowedGownPenalty)
class BorrowedGownPenaltyAdmin(admin.ModelAdmin):
	"""
		BorrowedGownPenalty Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'status')
	list_display = (
		'student', 'gown', 'penalty', 'balance', 'status', 'date_modified', 'date_created')
	search_fields = ('student__first_name', 'student__last_name', 'status__name')
