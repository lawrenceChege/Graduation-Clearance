from django.contrib import admin

from Records.models import Certificate, Distinction, Grade, ResultSlip


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
	"""
		Grade Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', )
	list_display = (
		'name', 'upper_marks', 'lower_marks', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'upper_marks', 'lower_marks', 'status__name')

@admin.register(Distinction)
class DistinctionAdmin(admin.ModelAdmin):
	"""
		Distinction Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', )
	list_display = (
		'name', 'upper_gpa', 'lower_gpa', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'upper_gpa', 'lower_gpa', 'status__name')

@admin.register(ResultSlip)
class ResultSlipAdmin(admin.ModelAdmin):
	"""
		ResultSlip Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'course', 'unit', 'grade')
	list_display = (
		'student', 'course', 'unit', 'grade', 'marks', 'status', 'date_modified', 'date_created')
	search_fields = ('student__first_name', 'student__last_name', 'course__name', 'unit__name', 'grade__name', 'status__name')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
	"""
		Certificate Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'course', 'distinction')
	list_display = (
		'student', 'course', 'distinction', 'status', 'date_modified', 'date_created')
	search_fields = ('student__first_name', 'student__last_name', 'course__name','distinction__name', 'status__name')