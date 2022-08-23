from django.contrib import admin
from Finance.models import Fee, StudentFee, StudentFeePayment


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
	"""
		Fee Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', )
	list_display = (
		'name', 'amount', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'amount', 'status__name')

@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
	"""
		StudentFee Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created','fee' )
	list_display = (
		'student', 'fee', 'amount_paid', 'balance', 'status', 'date_modified', 'date_created')
	search_fields = ('student__first_name', 'student__last_name' 'status__name')

@admin.register(StudentFeePayment)
class StudentFeePaymentAdmin(admin.ModelAdmin):
	"""
		StudentFeePayment Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'student_fee')
	list_display = (
		'student_fee', 'amount', 'receipt', 'status', 'date_modified', 'date_created')
	search_fields = ('receipt', 'status__name')
