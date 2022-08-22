"""
	Services for models of store module
"""


from Store.models import BorrowedGown, GraduationGown
from base.services.servicebase import ServiceBase


class GraduationGownService(ServiceBase):
	"""
		The service for handling CRUD events for the GraduationGown model
	"""
	manager = GraduationGown.objects


class BorrowedGownService(ServiceBase):
	"""
		The service for handling CRUD events for the orrowedGown model
	"""
	manager = BorrowedGown.objects


