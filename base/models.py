import uuid

from django.db import models


class BaseModel(models.Model):
	"""
	Define repetitive methods to enhance re-usability.
	"""
	synced = models.BooleanField(default=False)
	id = models.UUIDField(max_length=50, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
	date_modified = models.DateTimeField(auto_now=True)  # (default = timezone.now)
	date_created = models.DateTimeField(auto_now_add=True)  # (default = timezone.now)

	SYNC_MODEL = False

	class Meta(object):
		abstract = True


class GenericBaseModel(BaseModel):
	"""
	Define repetitive methods to avoid cycles of redefining in every model.
	"""
	name = models.CharField(max_length=35, null=False)
	description = models.TextField(max_length=255, blank=True, null=True)

	class Meta(object):
		abstract = True


class State(GenericBaseModel):
	"""
	States for objects lifecycle e.g. "Active", "Closed", etc
	"""

	def __str__(self):
		return '%s' % self.name

	SYNC_MODEL = True

	class Meta(object):
		ordering = ('name',)
		unique_together = ('name',)

	@classmethod
	def default_state(cls):
		"""
	The default Active state. Help in ensuring that the admin will be created without supplying the state at the
	command like.
	@return: The active state, if it exists, or create a new one if it doesn't exist.
	@rtype: str | None
	"""
		# noinspection PyBroadException
	
		state = cls.objects.get(name='Active')
		return state.id
	
	@classmethod
	def disabled_state(cls):
		"""
		The default Disabled state. Help in ensuring that the admin will be created without supplying the state at the
		command like.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException
	
		state = cls.objects.get(name='Disabled')
		return state