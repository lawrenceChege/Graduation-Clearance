"""
	Services for models of faulty module
"""


from Faculty.models import Course, Department, Faculty, HeadOfDepartment, Programme, Unit
from base.services.servicebase import ServiceBase


class ProgrammeService(ServiceBase):
	"""
		The service for handling CRUD events for the Programme model
	"""
	manager = Programme.objects


class FacultyService(ServiceBase):
	"""
		The service for handling CRUD events for the Faculty model
	"""
	manager = Faculty.objects

class DepartmentService(ServiceBase):
	"""
		The service for handling CRUD events for the Department model
	"""
	manager = Department.objects

class HeadOfDepartmentService(ServiceBase):
	"""
		The service for handling CRUD events for the head ofDepartment model
	"""
	manager = HeadOfDepartment.objects

class CourseService(ServiceBase):
	"""
		The service for handling CRUD events for the Course model
	"""
	manager = Course.objects

class UnitService(ServiceBase):
	"""
		The service for handling CRUD events for the unit model
	"""
	manager = Unit.objects

