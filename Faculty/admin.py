from django.contrib import admin
from Faculty.models import Course, Department, Faculty, HeadOfDepartment, Programme, Unit

# Register your models here.
@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
	"""
		Programme Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created',)
	list_display = (
		'name', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'status__name')


    # Register your models here.
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
	"""
		Faculty Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created',)
	list_display = (
		'name', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'status__name')

    # Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	"""
		Department Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'faculty')
	list_display = (
		'name', 'faculty', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'status__name')


@admin.register(HeadOfDepartment)
class HeadOfDepartmentAdmin(admin.ModelAdmin):
	"""
		HeadOfDepartment Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'department')
	list_display = (
		'department', 'head', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'head__username', 'head__first_name', 'head__last_name','status__name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	"""
		Course Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'level', 'department')
	list_display = (
		'name', 'description', 'department', 'level', 'program_goal', 'no_of_years', 'no_of_semesters',
        'minimum_requirement', 'fees', 'status', 'date_modified', 'date_created')
	search_fields = ('book__name', 'student__first_name', 'student__first_name','status__name')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
	"""
		Unit Model Admin
	"""
	ordering = ('-date_created',)
	list_filter = ('date_created', 'course')
	list_display = (
		'name', 'course', 'status', 'date_modified', 'date_created')
	search_fields = ('name', 'course__name', 'status__name')