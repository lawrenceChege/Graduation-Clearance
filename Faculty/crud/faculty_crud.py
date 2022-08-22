"""
This module will hold administration for Customer
"""
import random
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse

from audit.administration.audit_administration import TransactionLogBase
from base.backend.services import StateService, EntryChannelService, IdentityTypeService, BorrowerTypeService, \
	EducationLevelService
from base.backend.utils.commons import normalize_date
from base.backend.utils.validators import validate_uuid4
from customer.backend.services import CorporateCustomerService, CorporateCustomerTagService
from base.backend.utils.validators import validate_uuid4, validate_name, validate_phone_number, validate_email, \
	normalize_phone_number
from corporate.backend.services import CheckoffBranchService
from customer.backend.services import CorporateCustomerService, SegmentService
from euser.backend.services import EUserService
from corporate.backend.services import CorporateService, BranchService
from customer.backend.services import TagService
from euser.backend.services import EUserService


class CustomerAdministration(TransactionLogBase):
	"""
	Administration for the Customer
	"""

	def add_corporate_customer(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Creates a new CorporateCustomer in the system
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Add Customer", trace='customer/add_corporate_customer', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			first_name = kwargs.pop('first_name')
			last_name = kwargs.get('last_name')
			other_name = kwargs.get('other_name')
			salutation_id = kwargs.get('salutation')
			identity_type_id = kwargs.get('identity_type')
			identity_number = kwargs.pop('identity_number')
			gender = kwargs.get('gender')
			date_of_birth = kwargs.get('date_of_birth')
			email = kwargs.get('email')
			expiry_date_id = kwargs.get("passport_expiry_date")
			segment_id = kwargs.get("segment")
			relationship_officer_id = kwargs.get("relationship_officer")
			phone_number = kwargs.get("phone_number")
			education_level_id = kwargs.get("education_level")
			marital_status = kwargs.get("marital_status")
			borrower_type_id = kwargs.get("borrower_type")
			entry_channel_id = kwargs.pop("entry_channel")
			branch_id = kwargs.pop('branch')
			checkoff_branch_id = kwargs.get("checkoff_branch")
			k = {}
			if branch_id and not validate_uuid4(branch_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Branch')
				return {'code': '999.005.006', 'message': 'Branch not valid', 'transaction': str(transaction.id)}
			branch = BranchService().get(id=branch_id)
			if not branch:
				self.mark_transaction_failed(transaction, code='300.002.002', description='Branch not found')
				return {'code': '300.002.002', 'message': 'Branch not found', 'transaction_id': str(transaction.id)}
			k['branch'] = branch
			if checkoff_branch_id:
				if not validate_uuid4(checkoff_branch_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid checkoff branch')
					return {'code': '999.005.006', 'message': 'Invalid checkoff branch', 'transaction': str(transaction.id)}
				checkoff_branch = CheckoffBranchService().get(id=checkoff_branch_id)
				if not checkoff_branch:
					self.mark_transaction_failed(transaction, code='300.010.002', description='Check off branch not found')
					return {
						'code': '300.010.002', 'message': 'check off branch not found', 'transaction_id': str(transaction.id)}
				k['checkoff_branch'] = checkoff_branch
			phone_number = normalize_phone_number(phone_number)
			if not validate_phone_number(phone_number):
				self.mark_transaction_failed(transaction, code='999.004.006', description='Invalid phone number')
				return {
					'code': '999.004.006', 'message': 'Invalid phone number', 'transaction_id': str(transaction.id)}
			k['phone_number'] = phone_number
			if education_level_id:
				if not validate_uuid4(education_level_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid education level')
					return {
						'code': '999.005.006', 'message': 'Invalid education level', 'transaction': str(transaction.id)}
				education_level = EducationLevelService().get(id=education_level_id)
				if not education_level:
					self.mark_transaction_failed(
						transaction, code='100.027.002', description='Education level not found')
					return {'code': '100.027.002', 'message': 'Education level', 'transaction_id': str(transaction.id)}
				k['education_level'] = education_level
			if relationship_officer_id and not validate_uuid4(relationship_officer_id):
				self.mark_transaction_failed(
					transaction, code='999.005.006', description='Invalid relationship officer')
				return {
					'code': '999.005.006', 'message': 'Invalid relationship officer',
					'transaction': str(transaction.id)}
			relationship_officer = EUserService().get(id=relationship_officer_id, state__name='Active')
			if not relationship_officer:
				self.mark_transaction_failed(
					transaction, code='500.007.002', description='Relationship officer not found')
				return {
					'code': '500.007.002', 'message': 'Relationship officer not found',
					'transaction_id': str(transaction.id)}
			k['relationship_officer'] = relationship_officer
			if email and not validate_email(email):
				self.mark_transaction_failed(transaction, code='999.003.006', description='Invalid email')
				return {
					'code': '999.003.006', 'transaction_id': str(transaction.id),
					'message': 'Email is invalid. Provide email in format someone@somecompany.something'}
			k['email'] = str(email).lower()
			gender = str(gender).strip()
			if gender.lower() == 'male':
				k['gender'] = 'M'
			elif gender.lower() == 'female':
				k['gender'] = 'F'
			else:
				k['gender'] = 'O'
			k['salutation'] = "Mr" if not salutation_id else salutation_id
			k['marital_status'] = "Single" if not marital_status else marital_status
			if first_name and not validate_name(str(first_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid first name')
				return {'code': '999.002.006', 'message': 'First name is invalid.', 'transaction': str(transaction.id)}
			k['first_name'] = first_name.title().strip()
			if other_name and not validate_name(str(other_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid other name')
				return {'code': '999.002.006', 'message': 'Other name is invalid.', 'transaction': str(transaction.id)}
			k['other_name'] = other_name.title().strip()
			if last_name and not validate_name(str(last_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid last name')
				return {'code': '999.002.006', 'message': 'last name is invalid.', 'transaction': str(transaction.id)}
			k['last_name'] = last_name.title().strip()
			k['date_of_birth'] = normalize_date(date_of_birth)
			if borrower_type_id:
				if not validate_uuid4(borrower_type_id):
					self.mark_transaction_failed(
						transaction, code='999.005.006', description='Invalid borrower type')
					return {'code': '999.005.006', 'message': 'Invalid borrower type', 'transaction': str(transaction.id)}
				borrower_type = BorrowerTypeService().get(id=borrower_type_id)
				if not borrower_type:
					self.mark_transaction_failed(
						transaction, code='100.030.002', description='Borrower type not found')
					return {
						'code': '100.030.002', 'message': 'Borrower type not found',
						'transaction_id': str(transaction.id)}
				k['borrower_type'] = borrower_type
			if identity_type_id and not validate_uuid4(identity_type_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid identity type')
				return {'code': '999.005.006', 'message': 'Invalid identity type', 'transaction': str(transaction.id)}
			identity_type = IdentityTypeService().get(id=identity_type_id)
			if not identity_type:
				self.mark_transaction_failed(transaction, code='100.026.007', description='Identity type not found')
				return {
					'code': '100.026.007', 'message': 'Identity type not found', 'transaction_id': str(transaction.id)}
			k['identity_type'] = identity_type
			if identity_number:
				customer_exists = CorporateCustomerService().get(
					identity_type=identity_type, identity_number=identity_number, branch__corporate=branch.corporate)
				if customer_exists:
					self.mark_transaction_failed(transaction, code='400.005.007', description='Customer already exists')
					return {
						'code': '400.005.007', 'message': 'Customer already exists',
						'transaction_id': str(transaction.id)}
				k['identity_number'] = identity_number
			if expiry_date_id:
				k['passport_expiry_date'] = normalize_date(str(expiry_date_id))
			if entry_channel_id and not validate_uuid4(entry_channel_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid entry channel')
				return {'code': '999.005.006', 'message': 'Invalid entry channel', 'transaction': str(transaction.id)}
			entry_channel = EntryChannelService().get(id=entry_channel_id)
			if not entry_channel:
				self.mark_transaction_failed(transaction, code='100.008.002', description='Entry channel not found')
				return {
					'code': '100.008.002', 'message': 'Entry channel not found', 'transaction_id': str(transaction.id)}
			k['entry_channel'] = entry_channel
			if segment_id and not validate_uuid4(segment_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid segment')
				return {'code': '999.005.006', 'message': 'Invalid segment', 'transaction': str(transaction.id)}
			segment = SegmentService().get(id=segment_id)
			if not segment:
				self.mark_transaction_failed(transaction, code='400.002.002', description='Segment not found')
				return {'code': '400.002.002', 'message': 'Segment not found', 'transaction_id': str(transaction.id)}
			k['segment'] = segment
			state = StateService().get(name="Active")
			k['state'] = state
			corporate_customer = CorporateCustomerService().create(**k)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code="400.005.001", description='Failed to add Customer.')
				return {
					'code': '400.005.001', 'message': 'Failed to add customer.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'user': str(corporate_customer.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {
				"code": "999.999.999", 'message': "Error adding customer", 'transaction': str(transaction.id)}

	def update_corporate_customer(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Update  Customer information
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Edit Customer", trace='customer/update_corporate_customer', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			corporate_customer_id = kwargs.pop('customer')
			first_name = kwargs.get('first_name')
			last_name = kwargs.get('last_name')
			other_name = kwargs.get('other_name')
			salutation_id = kwargs.get('salutation')
			gender = kwargs.get('gender')
			date_of_birth = kwargs.get('date_of_birth')
			email = kwargs.get('email')
			expiry_date_id = kwargs.get("passport_expiry_date")
			segment_id = kwargs.get("segment")
			relationship_officer_id = kwargs.get("relationship_officer")
			phone_number = kwargs.get("phone_number")
			education_level_id = kwargs.get("education_level")
			marital_status = kwargs.get("marital_status")
			borrower_type_id = kwargs.get("borrower_type")
			branch_id = kwargs.get('branch')
			checkoff_branch_id = kwargs.get("checkoff_branch")
			k = {}
			if corporate_customer_id:
				if not validate_uuid4(corporate_customer_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
					return {'code': '999.005.006', 'message': 'Invalid customer', 'transaction': str(transaction.id)}
			corporate_customer = CorporateCustomerService().get(id=corporate_customer_id)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code='400.005.002', description='Customer not found')
				return {
					'code': '400.005.002', 'message': 'Customer not found', 'transaction': str(transaction.id)}
			if branch_id:
				if not validate_uuid4(branch_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Branch')
					return {'code': '999.005.006', 'message': 'Branch not valid', 'transaction': str(transaction.id)}
				branch = BranchService().get(id=branch_id)
				if not branch:
					self.mark_transaction_failed(transaction, code='300.002.002', description='Branch not found')
					return {'code': '300.002.002', 'message': 'Branch not found', 'transaction_id': str(transaction.id)}
				k['branch'] = branch
			if checkoff_branch_id:
				if not validate_uuid4(checkoff_branch_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid checkoff branch')
					return {'code': '999.005.006', 'message': 'Invalid checkoff branch', 'transaction': str(transaction.id)}
				checkoff_branch = CheckoffBranchService().get(id=checkoff_branch_id)
				if not checkoff_branch:
					self.mark_transaction_failed(transaction, code='300.010.002', description='Check off branch not found')
					return {
						'code': '300.010.002', 'message': 'Check off branch not found', 'transaction_id': str(transaction.id)}
				k['checkoff_branch'] = checkoff_branch
			phone_number = normalize_phone_number(phone_number)
			if phone_number:
				if not validate_phone_number(phone_number):
					self.mark_transaction_failed(transaction, code='999.004.006', description='Invalid phone number')
					return {
						'code': '999.004.006', 'message': 'Invalid phone number', 'transaction_id': str(transaction.id)}
				k['phone_number'] = phone_number
			if education_level_id:
				if not validate_uuid4(education_level_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid education level')
					return {
						'code': '999.005.006', 'message': 'Invalid education level', 'transaction': str(transaction.id)}
				education_level = EducationLevelService().get(id=education_level_id, state__name='Active')
				if not education_level:
					self.mark_transaction_failed(transaction, code='100.027.002', description='Education level not found')
					return {'code': '100.027.002', 'message': 'Education level not found', 'transaction_id': str(transaction.id)}
				k['education_level'] = education_level
			if relationship_officer_id:
				if not validate_uuid4(relationship_officer_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid relationship officer')
					return {
						'code': '999.005.006', 'message': 'Invalid relationship officer',
						'transaction': str(transaction.id)}
				relationship_officer = EUserService().get(id=relationship_officer_id, state__name='Active')
				if not relationship_officer:
					self.mark_transaction_failed(
						transaction, code='500.007.002', description='Relationship officer not found')
					return {
						'code': '500.007.002', 'message': 'Relationship officer not found',
						'transaction_id': str(transaction.id)}
				k['relationship_officer'] = relationship_officer
			if email:
				if not validate_email(email):
					self.mark_transaction_failed(transaction, code='999.003.006', description='Invalid email')
					return {
						'code': '999.003.006', 'transaction_id': str(transaction.id),
						'message': 'Email is invalid. Provide email in format someone@somecompany.something'}
				k['email'] = str(email).lower()
			gender = str(gender).strip()  # Some BS somewhere sending us some S!
			if gender.lower() == 'male':
				k['gender'] = 'M'
			elif gender.lower() == 'female':
				k['gender'] = 'F'
			elif gender.lower() == 'other':
				k['gender'] = 'O'
			k['salutation'] = "Mr" if not salutation_id else salutation_id
			k['marital_status'] = marital_status
			if first_name:
				if not validate_name(str(first_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid first name')
					return {'code': '999.002.006', 'message': 'First name is invalid.', 'transaction': str(transaction.id)}
				k['first_name'] = first_name.title().strip()
			if other_name:
				if not validate_name(str(other_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid other name')
					return {'code': '999.002.006', 'message': 'Other name is invalid.', 'transaction': str(transaction.id)}
				k['other_name'] = other_name.title().strip()
			if last_name:
				if not validate_name(str(last_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid last name')
					return {'code': '999.002.006', 'message': 'last name is invalid.', 'transaction': str(transaction.id)}
				k['last_name'] = last_name.title().strip()
			if date_of_birth:
				k['date_of_birth'] = normalize_date(str(date_of_birth))
			if borrower_type_id:
				if not validate_uuid4(borrower_type_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid borrower type')
					return {'code': '999.005.006', 'message': 'Invalid borrower type', 'transaction': str(transaction.id)}
				borrower_type = BorrowerTypeService().get(id=borrower_type_id)
				if not borrower_type:
					self.mark_transaction_failed(transaction, code='100.030.002', description='Borrower type not found')
					return {
						'code': '100.030.002', 'message': 'Borrower type not found',
						'transaction_id': str(transaction.id)}
				k['borrower_type'] = borrower_type
			if expiry_date_id:
				k['passport_expiry_date'] = normalize_date(str(expiry_date_id))
			if segment_id:
				if not validate_uuid4(segment_id):
					self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid segment')
					return {'code': '999.005.006', 'message': 'Invalid segment', 'transaction': str(transaction.id)}
				segment = SegmentService().get(id=segment_id)
				if not segment:
					self.mark_transaction_failed(transaction, code='400.002.002', description='Segment not found')
					return {
						'code': '400.002.002', 'message': 'Segment not found', 'transaction_id': str(transaction.id)}
				k['segment'] = segment
			corporate_customer = CorporateCustomerService().update(pk=corporate_customer.id, **k)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code="400.005.001", description='Failed to update customer.')
				return {
					'code': '400.005.001', 'message': 'Failed to update customer.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'customer': corporate_customer.id}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {
				"code": "999.999.999", 'message': "Error updating customer", 'transaction': str(transaction.id)}

	def disable_corporate_customer(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles disabling of corporate customer
		@params request: Http request
		@type request: HttpRequest
		@params kwargs: Key value object containing the data
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Disable Customer", trace='customer/disable_corporate_customer', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			corporate_customer_id = kwargs.pop('customer')
			if not validate_uuid4(corporate_customer_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
				return {'code': '999.005.006', 'message': 'Invalid customer', 'transaction': str(transaction.id)}
			active = StateService().get(name="Active")
			suspended = StateService().get(name="Suspended")
			corporate_customer = CorporateCustomerService().get(
				Q(state=active) | Q(state=suspended), pk=corporate_customer_id)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code='400.005.002', description='Customer not found')
				return {'code': '400.005.002', 'message': 'Customer not found', 'transaction': str(transaction.id)}
			disabled = StateService().get(name="Disabled")
			corporate_customer = CorporateCustomerService().update(pk=corporate_customer.id, state=disabled)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code="400.005.007", description='Failed to disable customer.')
				return {
					'code': '400.005.007', 'message': 'Failed to disable customer.', 'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'customer': str(corporate_customer.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {'code': '999.999.999', 'message': 'Error disabling customer', 'transaction': str(transaction.id)}

	def enable_corporate_customer(
			self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles enabling of corporate customer
		@params request: Http request
		@type request: HttpRequest
		@params kwargs: Key value object containing the data
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Enable Customer", trace='customer/enable_corporate_customer', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			corporate_customer_id = kwargs.pop('customer')
			if not validate_uuid4(corporate_customer_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
				return {
					'code': '999.005.006', 'message': 'Invalid customer', 'transaction': str(transaction.id)}
			disabled = StateService().get(name="Disabled")
			suspended = StateService().get(name="Suspended")
			corporate_customer = CorporateCustomerService().get(
				Q(state=disabled) | Q(state=suspended), pk=corporate_customer_id)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code='400.005.002', description='Customer not found')
				return {
					'code': '400.005.002', 'message': 'Customer not found',
					'transaction': str(transaction.id)}
			active = StateService().get(name="Active")
			corporate_customer = CorporateCustomerService().update(pk=corporate_customer.id, state=active)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code="400.005.007", description='Failed to enable customer.')
				return {
					'code': '100.001.001', 'message': 'Failed to enable customer.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {
				'code': '100.000.000', 'message': 'Success', 'data': {'customer': str(corporate_customer.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error enabling customer',
				'transaction': str(transaction.id)}

	def delete_corporate_customer(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles deleting of corporate customer
		@params request: Http request
		@type request: HttpRequest
		@params kwargs: Key value object containing the data
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Delete Customer", trace='customer/delete_corporate_customer', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			corporate_customer_id = kwargs.pop('customer')
			if not validate_uuid4(corporate_customer_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
				return {
					'code': '999.005.006', 'message': 'Invalid customer', 'transaction': str(transaction.id)}
			deleted = StateService().get(name="Deleted")
			corporate_customer = CorporateCustomerService().filter(~Q(state=deleted), pk=corporate_customer_id).first()
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code='400.005.002', description='Customer not found')
				return {
					'code': '400.005.002', 'message': 'Customer not found',
					'transaction': str(transaction.id)}
			corporate_customer = CorporateCustomerService().update(pk=corporate_customer.id, state=deleted)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code="400.005.007", description='Failed to delete customer.')
				return {
					'code': '400.005.007', 'message': 'Failed to delete customer.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {
				'code': '100.000.000', 'message': 'Success', 'data': {'customer': str(corporate_customer.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error deleting customer', 'transaction': str(transaction.id)}

	def freeze_corporate_customer(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles freezing of an active corporate customer
		@params request: Http request
		@type request: HttpRequest
		@params kwargs: Key value object containing the data
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Freeze Customer", trace='customer/freeze_corporate_customer', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			corporate_customer_id = kwargs.pop('customer')
			if not validate_uuid4(corporate_customer_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
				return {'code': '999.005.006', 'message': 'Invalid customer', 'transaction': str(transaction.id)}
			corporate_customer = CorporateCustomerService().get(pk=corporate_customer_id)
			if not corporate_customer:
				self.mark_transaction_failed(transaction, code='400.005.002', description='Customer not found')
				return {'code': '400.005.002', 'message': 'Customer not found', 'transaction': str(transaction.id)}
			state_active = StateService().get(name="Active")
			corporate_customer = CorporateCustomerService().update(pk=corporate_customer.id, state=state_active, freeze=True)
			if not corporate_customer:
				self.mark_transaction_failed(transaction, code="400.005.001", description='Failed to freeze customer.')
				return {
					'code': '400.005.001', 'message': 'Failed to freeze customer.', 'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'customer': str(corporate_customer.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {'code': '999.999.999', 'message': 'Error freezing customer', 'transaction': str(transaction.id)}

	def unfreeze_corporate_customer(
			self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles unfreezing of an active corporate customer
		@params request: Http request
		@type request: HttpRequest
		@params kwargs: Key value object containing the data
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Unfreeze Customer", trace='customer/unfreeze_corporate_customer',
			request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			corporate_customer_id = kwargs.pop('customer')
			if not validate_uuid4(corporate_customer_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
				return {
					'code': '999.005.006', 'message': 'Invalid customer',
					'transaction': str(transaction.id)}
			corporate_customer = CorporateCustomerService().get(pk=corporate_customer_id)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code='400.005.002', description='Customer not found')
				return {
					'code': '400.005.002', 'message': 'Customer not found',
					'transaction': str(transaction.id)}
			corporate_customer = CorporateCustomerService().update(
				pk=corporate_customer.id, freeze=False)
			if not corporate_customer:
				self.mark_transaction_failed(
					transaction, code="400.005.001", description='Failed to unfreeze customer.')
				return {
					'code': '400.005.001', 'message': 'Failed to unfreeze customer.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {
				'code': '100.000.000', 'message': 'Success', 'data': {'customer': str(corporate_customer.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error unfreezing customer',
				'transaction': str(transaction.id)}

	def add_corporate_tag(self, request, **data) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles adding of corporate tag
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Add Corporate Tag", trace='customer/add_corporate_tag', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			name = data.pop('name')
			description = data.get('description')
			corporate_id = data.pop('corporate')
			data = {}
			if not validate_name(name):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid tag name')
				return {'code': '999.002.006', 'message': 'Tag name is invalid.', 'transaction': str(transaction.id)}
			if not validate_uuid4(corporate_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid corporate')
				return {'code': '999.005.006', 'message': 'Corporate not valid', 'transaction': str(transaction.id)}
			corporate = CorporateService().get(pk=corporate_id)
			if not corporate:
				self.mark_transaction_failed(transaction, code='300.001.002', description='Corporate not found')
				return {'code': '300.001.002', 'message': 'Corporate not found', 'transaction_id': str(transaction.id)}
			tag = TagService().get(name=name.strip(), corporate=corporate)
			if tag:
				self.mark_transaction_failed(transaction, code='400.003.003', description='Tag already exists')
				return {'code': '400.003.003', 'message': 'Tag already exists', 'transaction_id': str(transaction.id)}
			data['name'] = name
			data['corporate'] = corporate
			data['state'] = StateService().get(name='Active')
			if description:
				data['description'] = description
			corporate_tag = TagService().create(**data)
			if not corporate_tag:
				self.mark_transaction_failed(transaction, code="400.003.001", description='Failed to add corporate tag.')
				return {
					'code': '400.003.001', 'message': 'Failed to add corporate tag.', 'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'Tag': str(corporate_tag.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse({
				'code': '999.999.999', 'message': 'Error adding corporate Tag', 'transaction': str(transaction.id)})

	def update_corporate_tag(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles update of corporate tag
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Update Corporate Tag", trace='customer/update_corporate_tag', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			tag_id = kwargs.pop('tag')
			name = kwargs.get('name')
			description = kwargs.get('description')
			corporate_id = kwargs.pop('corporate')
			data = {}
			if not validate_uuid4(corporate_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid corporate')
				return {'code': '999.005.006', 'message': 'Corporate not valid', 'transaction': str(transaction.id)}
			corporate = CorporateService().get(pk=corporate_id)
			if not corporate:
				self.mark_transaction_failed(transaction, code='300.001.002', description='Corporate not found')
				return {'code': '300.001.002', 'message': 'Corporate not found', 'transaction_id': str(transaction.id)}
			if not validate_uuid4(tag_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid tag')
				return {'code': '999.005.006', 'message': 'Tag is invalid.', 'transaction': str(transaction.id)}
			tag = TagService().get(pk=tag_id, corporate=corporate)
			if not tag:
				self.mark_transaction_failed(transaction, code='400.003.002', description='Tag not found')
				return {'code': '400.003.002', 'message': 'Tag not found', 'transaction': str(transaction.id)}
			if name:
				if not validate_name(name, 2):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid tag name')
					return {'code': '999.002.006', 'message': 'Tag name is invalid.', 'transaction': str(transaction.id)}
				data['name'] = str(name).strip().title()
			if description:
				data['description'] = description
			corporate_tag = TagService().update(pk=tag.id, **data)
			if not corporate_tag:
				self.mark_transaction_failed(transaction, code="400.003.001", description='Failed to update corporate tag.')
				return {'code': '400.003.001', 'message': 'Failed to update corporate tag.', 'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'Tag': str(corporate_tag.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse(
				{'code': '999.999.999', 'message': 'Error update corporate Tag', 'transaction': str(transaction.id)})

	def remove_corporate_tag(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles removal of corporate tag
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Remove Corporate Tag", trace='customer/remove_corporate_tag',	request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			tag_id = kwargs.pop('tag')
			corporate_id = kwargs.pop('corporate')
			if not validate_uuid4(corporate_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid corporate')
				return {'code': '999.005.006', 'message': 'Corporate not valid', 'transaction': str(transaction.id)}
			corporate = CorporateService().get(pk=corporate_id)
			if not corporate:
				self.mark_transaction_failed(transaction, code='300.001.002', description='Corporate not found')
				return {'code': '300.001.002', 'message': 'Corporate not found', 'transaction_id': str(transaction.id)}
			if not validate_uuid4(tag_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid tag')
				return {'code': '999.005.006', 'message': 'Tag is invalid.', 'transaction': str(transaction.id)}
			tag = TagService().get(pk=tag_id, corporate=corporate)
			if not tag:
				self.mark_transaction_failed(transaction, code='400.003.002', description='Tag not found')
				return {'code': '400.003.002', 'message': 'Tag not found', 'transaction': str(transaction.id)}
			deleted = StateService().get(name="Deleted")
			removed = TagService().update(pk=tag.id, state=deleted)
			if not removed:
				self.mark_transaction_failed(
					transaction, code="400.003.001", description='Failed to remove corporate tag.')
				return {
					'code': '400.003.001', 'message': 'Failed to update corporate tag.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'Tag': str(removed.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error removing corporate Tag', 'transaction': str(transaction.id)}

	def disable_corporate_tag(self, request, **data) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles disabling of corporate tag
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Disable Corporate Tag", trace='customer/disable_corporate_tag', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			tag_id = data.pop('tag')
			if not validate_uuid4(tag_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Tag id')
				return {'code': '999.005.006', 'message': 'Tag id not valid', 'transaction': str(transaction.id)}
			state = StateService().get(name='Active')
			if not state:
				self.mark_transaction_failed(transaction, code='100.001.001', description='State not found')
				return {'code': '100.001.001', 'message': 'State not found', 'transaction_id': str(transaction.id)}
			tag = TagService().get(pk=tag_id, state=state)
			if not tag:
				self.mark_transaction_failed(transaction, code='400.003.002', description='Tag not found')
				return {'code': '400.003.002', 'message': 'Tag not found', 'transaction_id': str(transaction.id)}
			disabled = StateService().get(name='Disabled')
			if not disabled:
				self.mark_transaction_failed(transaction, code='100.001.002', description='State not found')
				return {'code': '100.001.002', 'message': 'State not found', 'transaction_id': str(transaction.id)}
			corporate_tag = TagService().update(pk=tag_id, state=disabled)
			if not corporate_tag:
				self.mark_transaction_failed(transaction, code="400.003.001", description='Failed to disable corporate tag.')
				return {
					'code': '400.003.001', 'message': 'Failed to disable corporate tag.','transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'Tag': str(corporate_tag.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse({
				'code': '999.999.999', 'message': 'Error adding corporate Tag', 'transaction': str(transaction.id)})

	def enable_corporate_tag(self,  request, **data) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles enable of corporate tag
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Enable Corporate Tag", trace='customer/enable_corporate_tag', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			tag_id = data.pop('tag')
			disabled = StateService().get(name='Disabled')
			suspended = StateService().get(name='Suspended')
			active = StateService().get(name='Active')
			if not validate_uuid4(tag_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Tag id')
				return {'code': '999.005.006', 'message': 'Tag id not valid', 'transaction': str(transaction.id)}
			tag = TagService().get(Q(state=disabled) | Q(state=suspended), pk=tag_id)
			if not tag:
				self.mark_transaction_failed(transaction, code='400.003.002', description='Tag not found')
				return {'code': '400.003.002', 'message': 'Tag not found', 'transaction_id': str(transaction.id)}
			corporate_tag = TagService().update(pk=tag.id, state=active)
			if not corporate_tag:
				self.mark_transaction_failed(transaction, code="400.003.001",description='Failed to enable corporate tag.')
				return {
					'code': '400.003.001', 'message': 'Failed to enable corporate tag.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'Tag': str(corporate_tag.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse({
				'code': '999.999.999', 'message': 'Error adding corporate Tag', 'transaction': str(transaction.id)})

	def tag_corporate_customer(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles tagging corporate customer
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Tag Customer", trace='customer/tag_corporate_corporate', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			corporate_customer_id = kwargs.pop('customer')
			tag_id = kwargs.pop('tag')
			k = {}
			if not validate_uuid4(corporate_customer_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
				return {
					'code': '999.005.006', 'message': 'Invalid customer', 'transaction': str(transaction.id)}
			corporate_customer = CorporateCustomerService().get(pk=corporate_customer_id)
			if not corporate_customer:
				self.mark_transaction_failed(transaction, code='400.005.002', description='Customer not found')
				return {'code': '400.005.002', 'message': 'Customer not found', 'transaction': str(transaction.id)}
			k['corporate_customer'] = corporate_customer
			if not validate_uuid4(tag_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Tag id')
				return {'code': '999.005.006', 'message': 'Tag id not valid', 'transaction': str(transaction.id)}
			tag = TagService().get(pk=tag_id)
			if not tag:
				self.mark_transaction_failed(transaction, code='400.003.002', description='Tag not found')
				return {'code': '400.003.002', 'message': 'Tag not found', 'transaction_id': str(transaction.id)}
			k['tag'] = tag
			customer_already_tagged = CorporateCustomerTagService().get(
				corporate_customer=corporate_customer, tag=tag)
			if customer_already_tagged:
				self.mark_transaction_failed(transaction, code='400.006.003', description='Customer already tagged')
				return {
					'code': '400.006.003', 'message': 'Customer already tagged', 'transaction_id': str(transaction.id)}
			active = StateService().get(name='Active')
			k['state'] = active
			customer_tag = CorporateCustomerTagService().create(**k)
			if not customer_tag:
				self.mark_transaction_failed(
					transaction, code='400.006.001', description='Failed to tag customer')
				return {
					'code': '400.006.001', 'message': 'Failed to tag customer',
					'transaction_id': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {
				'code': '100.000.000', 'message': 'Success', 'data': {'customer_tag': str(customer_tag.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error tagging customer', 'transaction': str(transaction.id)}

	def untag_corporate_customer(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles untagging  customer
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Untag Customer", trace='customer/untag_corporate_customer', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			tag_id = kwargs.pop('tag')
			customer_id = kwargs.pop('customer')
			deleted = StateService().get(name="Deleted")
			if not validate_uuid4(customer_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid customer')
				return {
					'code': '999.005.006', 'message': 'Invalid customer', 'transaction': str(transaction.id)}
			corporate_customer = CorporateCustomerService().get(pk=customer_id)
			if not corporate_customer:
				self.mark_transaction_failed(transaction, code='400.005.002', description='Customer not found')
				return {
					'code': '400.005.002', 'message': 'Customer not found', 'transaction': str(transaction.id)}
			if not validate_uuid4(tag_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Tag')
				return {'code': '999.005.006', 'message': 'Tag not valid', 'transaction': str(transaction.id)}
			tag = TagService().get(pk=tag_id)
			if not tag:
				self.mark_transaction_failed(transaction, code='400.003.002', description='Tag not found')
				return {'code': '400.003.002', 'message': 'Tag not found', 'transaction_id': str(transaction.id)}
			corporate_customer_tag = CorporateCustomerTagService().get(tag=tag, corporate_customer=corporate_customer)
			if not corporate_customer_tag:
				self.mark_transaction_failed(transaction, code='400.006.002', description='Customer Tag not found')
				return {'code': '400.006.002', 'message': 'Customer Tag not found', 'transaction_id': str(transaction.id)}
			customer_tag = CorporateCustomerTagService().update(pk=corporate_customer_tag.id, state=deleted)
			if not customer_tag:
				self.mark_transaction_failed(transaction, code='400.006.007', description='Customer Tag not found')
				return {'code': '400.006.007', 'message': 'Customer Tag not found', 'transaction_id': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success'}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error removing customer tag', 'transaction': str(transaction.id)}