"""
	Services for models of finance module
"""


from Faculty.models import StudentFeePayment, StudentFee, Fee
from base.services.servicebase import ServiceBase


class FeeService(ServiceBase):
	"""
		The service for handling CRUD events for the Fee model
	"""
	manager = Fee.objects


class StudentFeeService(ServiceBase):
	"""
		The service for handling CRUD events for the StudentFee model
	"""
	manager = StudentFee.objects


class StudentFeePaymentService(ServiceBase):
	"""
		The service for handling CRUD events for the StudentFeePayment model
	"""
	manager = StudentFeePayment.objects


