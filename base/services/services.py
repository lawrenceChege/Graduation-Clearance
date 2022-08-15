from base.models import State
from base.services.servicebase import ServiceBase


class StateService(ServiceBase):
	"""
		The service for handling CRUD events for the State model
	"""
	manager = State.objects