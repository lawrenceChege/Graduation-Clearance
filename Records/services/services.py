"""
	Services for models of records module
"""


from Records.models import Certificate, ResultSlip
from base.services.servicebase import ServiceBase


class ResultSlipService(ServiceBase):
	"""
		The service for handling CRUD events for the ResultSlip model
	"""
	manager = ResultSlip.objects


class CertificateService(ServiceBase):
	"""
		The service for handling CRUD events for the Certificate model
	"""
	manager = Certificate.objects


