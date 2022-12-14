"""
	This module defines CRUD services applied on models.
"""
import logging
from django.db.models.query import QuerySet

lgr = logging.getLogger(__name__)


class ServiceBase:
	"""
	This class handles CRUD methods for all models
	The manager represents the manager for the given module
	"""
	manager = None
	using = "default"

	def __init__(self, lock_for_update=False, *args, **annotations):
		"""
			This method initializes the class.
			@param lock_for_update: A sentinel determining whether to lock this model.
			@type lock_for_update: bool default=False.
			@param args: Strictly ordered arguments to be provided in the respective order.
			@param annotations: Key-word arguments to help with DT annotated fields as they are searchable.
		"""
		super(ServiceBase, self).__init__()
		if lock_for_update and self.manager is not None:
			self.manager = self.manager.select_for_update()
		if args:  # Try set up ordered tuples
			for arg in args:
				if isinstance(arg, tuple):
					try:
						n_dict = {'%s' % arg[0]: arg[1]}
						self.manager = self.manager.annotate(**n_dict)
					except Exception as e:
						print('Initializing Annotations Error: %s' % e)
		if annotations:
			self.manager = self.manager.annotate(**annotations)

	def get(self, *args, **kwargs):
		"""
			This method retrieves a single record from the Database using the manager.
			@params args: Arguments to pass the get method.
			@params kwargs: Key-Value arguments to pass the get method.
			@return Queryset; Manager object instance or None on error
		"""
		try:
			if self.manager is not None:
				return self.manager.get(*args, **kwargs)
		except self.manager.model.DoesNotExist as E_404:
			pass
		except Exception as e:
			lgr.exception('%s Service get exception: %s' % (self.manager.model.__name__, e))
		return None

	def filter(self, *args, **kwargs) -> 'QuerySet[self.manager.model.__name__]':
		"""
			This method filters through a model using given parameters
			@param args: Arguments to pass to the filter method
			@param kwargs: Key-Value arguments to pass to the filter method
			@return Queryset: Queryset or None on error
			@rtype: Queryset |None
		"""
		try:
			if self.manager is not None:
				return self.manager.filter(*args, **kwargs)
		except self.manager.model.DoesNotExist:
			pass
		except Exception as e:
			lgr.exception('%s Service filter exception: %s' % (self.manager.model.__name__, e))
		return None

	def create(self, **kwargs) -> 'QuerySet[self.manager.model.__name__]':
		"""
			This method creates an entry in the database.
			@params Kwargs: Key-value arguments used to create a record in the database.
			Key refers to the column in the database and Value refers to the value to be added in the column
			@return Queryset: The created object of None on error
		"""
		try:
			if 'pk' in kwargs and self.manager.get(pk=kwargs.get('pk', '')):
				return self.manager.get(pk=kwargs.get('pk', ''))
			if self.manager is not None:
				return self.manager.create(**kwargs)
		except Exception as e:
			lgr.exception('%s Service create exception: %s' % (self.manager.model.__name__, e))
		return None

	def update(self, pk, **kwargs) -> 'QuerySet[self.manager.model.__name__]':
		"""
			This method updates a specific record with given Key
		"""
		try:
			record = self.get(id=pk)
			if record is not None:
				for k, v in kwargs.items():
					setattr(record, k, v)
				record.save(using=self.using)
				record.refresh_from_db()
				return record
		except Exception as e:
			lgr.exception('%sService update exception: %s' % (self.manager.model.__name__, e))
		return None
