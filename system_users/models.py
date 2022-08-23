"""
	module for SUsers
"""

from base.models import GenericBaseModel, State, BaseModel

import unicodedata
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
	check_password, is_password_usable, make_password,
)
# from django.contrib.auth.models import user_get_all_permissions, _user_has_perm, _user_has_module_perms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import salted_hmac
from django.utils.encoding import  force_str
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import _user_get_permissions, _user_has_perm, _user_has_module_perms

from django.utils import timezone

# from corporate.models import Branch, Corporate, CheckoffBranch
from system_users.backend.managers import SUserManager


class Role(GenericBaseModel):
	"""
		model for roles
	"""
	is_staff_role = models.BooleanField(default=False)
	is_super_admin_role = models.BooleanField(default=False)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % self.name

	def __repr__(self):
		return f'Role_name={self.name},Is_staff_role={self.is_staff_role},Is_service_provider_role={self.is_service_provider_role},Is_super_admin={self.is_super_admin_role}'

	class Meta(object):
		unique_together = ('name',)


class Permission(GenericBaseModel):
	"""
		This model handles system user  permission.
	"""
	parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
	simple_name = models.TextField(max_length=255, blank=True, null=True)
	extendable = models.BooleanField(default=False)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '%s' % self.name

	def __repr__(self):
		return f'Permission_name = {self.name},simple_name = {self.simple_name}'

	class Meta(object):
		""" model  meta data"""
		unique_together = ('name',)


class RolePermission(BaseModel):
	"""
	This model maps different system roles with assigned permissions
	"""
	role = models.ForeignKey(Role, on_delete=models.CASCADE)
	permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '%s %s' % (self.role.name, self.permission.name)

	def __repr__(self):
		return f'role_name = {self.role.name}, permission_name={self.permission.name}'

	class Meta(object):
		unique_together = ('role', 'permission')


class SUserPassword(BaseModel):
	"""
	This model manages the user credentials. i.e:
		user(FK),password,state(FK)
	@note: Needs to be here to be used in the base class implementation.
	"""
	SUser = models.ForeignKey('SUser', related_name='user_passwords', on_delete=models.CASCADE)
	password = models.CharField(_('password'), max_length=128)
	hashed_password = models.BooleanField(_('is password hashed'), default=False, editable=False)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	class Meta(object):
		ordering = ('-date_created',)
		verbose_name = 'Password'
		verbose_name_plural = 'Passwords'

	def __str__(self):
		return self.password


# noinspection PyUnusedLocal
@receiver(post_save, sender=SUserPassword)
def hash_set_password(sender, instance, created, **kwargs):
	"""
		When the object is created, hash the password.
	"""
	if created and not instance.hashed_password:
		instance.hashed_password = True
		instance.password = make_password(instance.password)
		instance.save()


class SUserSecurityQuestion(BaseModel):
	"""
		This model manages the users' security questions and security_question answers
	"""
	SUser = models.ForeignKey('SUser', related_name='user_questions',on_delete=models.CASCADE)
	security_question = models.TextField(max_length=50)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
	answer_hash = models.CharField(max_length=255)

	def __str__(self):
		return '%s %s %s' % (self.SUser, self.security_question, self.state)

	class Meta(BaseModel.Meta):
		ordering = ('-date_created',)


class AbstractSUser(models.Model):
	"""
		The base model for the e user.
	"""
	last_login = models.DateTimeField(_('last login'), blank=True, null=True)

	is_active = True

	USERNAME_FIELD = None

	EMAIL_FIELD = None

	REQUIRED_FIELDS = []

	class Meta(object):
		abstract = True

	def get_username(self):
		"""
		Return the identifying username for this User
		"""
		return getattr(self, self.USERNAME_FIELD)

	def __init__(self, *args, **kwargs):
		super(AbstractSUser, self).__init__(*args, **kwargs)
		# Stores the raw password if set_password() is called so that it can
		# be passed to password_changed() after the model is saved.
		self._password = None

	def __str__(self):
		return self.get_username()

	def clean(self):
		"""Clean the username field"""
		setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

	def save(self, *args, **kwargs):
		"""Override to save the user with some magic"""
		super(AbstractSUser, self).save(*args, **kwargs)
		if self._password is not None:
			password_validation.password_changed(self._password, self)
			self._password = None

	def natural_key(self):
		"""Retrieve the username for the model"""
		return self.get_username(),

	@property
	def is_anonymous(self):
		"""
		Always return False. This is a way of comparing User objects to
		anonymous users.
		"""
		return  False

	@property
	def is_authenticated(self):
		"""
		Always return True. This is a way to tell if the user has been
		authenticated in templates.
		"""
		return True

	@property
	def password(self):
		"""Returns the most recent active password for the user or None"""
		# noinspection PyBroadException
		try:
			return SUserPassword.objects.filter(SUser=self, state__name='Active').order_by('-date_created').first()
		except Exception as e:
			return e

	
	# noinspection PyBroadException
	def set_password(self, raw_password):
		"""
		Sets the password for the user by creating a new active user password entry for the user instance
		@param raw_password: The raw password we are setting.
		@type raw_password: str
		"""
		try:
			self.save()  # Save our current model
			pass_update = SUserPassword.objects.create(
				SUser=self, password=make_password(raw_password), state_id=State.default_state(), hashed_password
				=True)
			if pass_update is not None:
				SUserPassword.objects.filter(
					~Q(pk=pass_update.pk), SUser=self, state__name='Active').update(
					state=State.disabled_state())
			if pass_update is not None:
				self._password = raw_password
		except Exception as e:
			print('Exception: %s' % e)

	
	

	def check_password(self, raw_password):
		"""
		Return a boolean of whether the raw_password was correct. Handles
		hashing formats behind the scenes.
		"""

		# noinspection PyUnusedLocal,PyShadowingNames
		def setter(raw_password):
			"""Sets the new password"""
			self.set_password(raw_password)
			# Password hash upgrades shouldn't be considered password changes.
			self._password = None
			self.save()

		return check_password(raw_password, str(self.password), setter)

	def set_unusable_password(self):
		"""Set a value that will never be a valid hash"""
		self._password = make_password(None)

	def has_usable_password(self):
		"""Checks if the password is usable"""
		return is_password_usable(str(self.password))

	def get_full_name(self):
		"""Retrieve the full name for the user"""
		raise NotImplementedError('subclasses of AbstractSUser must provide a get_full_name() method')

	def get_short_name(self):
		"""Retrieve a short name for the user"""
		raise NotImplementedError('subclasses of AbstractSUser must provide a get_short_name() method.')

	def get_session_auth_hash(self):
		"""
		Return an HMAC of the password field.
		"""
		key_salt = "SUser.models.AbstractSUser.get_session_auth_hash"
		return salted_hmac(key_salt, self._password).hexdigest()

	@classmethod
	def get_email_field_name(cls):
		"""Get the email field name"""
		try:
			return cls.EMAIL_FIELD
		except AttributeError:
			return 'email'

	@classmethod
	def normalize_username(cls, username):
		"""Normalize the username"""
		return unicodedata.normalize('NFKC', force_str(username))


class SUser(BaseModel, AbstractSUser):
	"""
	The class that manages User data for access and association with corporates.
	"""
	username = models.CharField(
		max_length=50, unique=True,
		help_text='System-wide identifier used to identify the admin for authentication')
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	phone_number = models.CharField(_('phone number'), max_length=20)
	email = models.CharField(max_length=50)
	state = models.ForeignKey(State, default=State.default_state,on_delete=models.CASCADE)
	is_active = models.BooleanField(_('active'), default=True, help_text='User is currently active.')
	is_staff = models.BooleanField(_('staff'), default=False, help_text='User can login login to the dashboard.')
	is_superuser = models.BooleanField(
		_('super user'), default=False, help_text='User has full permissions on the admin dashboard.')
	last_activity = models.DateTimeField(_('last activity'), null=True, blank=True, editable=False)
	role = models.ForeignKey(
		Role, related_name='roles', null=True, blank=True,
		help_text='The role for the user belongs to. Cannot be null unless super user',on_delete=models.CASCADE)
	# Only null if the user is a super user.
	permissions = models.ManyToManyField(
		Permission, through='ExtendedSUserPermission', blank=True, related_name="SUser_set",
		related_query_name="SUser", help_text='Specific permissions for this user.')

	SYNC_MODEL = True

	EMAIL_FIELD = 'email'

	USERNAME_FIELD = 'username'

	REQUIRED_FIELDS = ['phone_number', 'email']

	objects = SUserManager()

	def __str__(self):
		return '%s %s - %s' % (self.branch, self.username, self.role)

	def update_last_activity(self):
		"""
			Update the last time the user was activity
		"""
		self.last_activity = timezone.now()
		self.save(update_fields=["last_activity"])

	def clean(self):
		"""
			Custom validation for the fields.
		"""
		if (self.branch is None or self.role is None) and not self.is_superuser:
			raise ValidationError('To clean, a user MUST have a role and branch!')
		super(SUser, self).clean()

	def save(self, *args, **kwargs):
		"""
			Override save method  to ensure valid Users have been saved.
		"""
		if (self.branch is None or self.role is None) and not self.is_superuser:
			raise ValidationError('To save, a user MUST have a role and branch!')
		super(SUser, self).save(*args, **kwargs)

	def get_full_name(self):
		"""
			Retrieves the full name for the model
		"""
		return '%s - %s %s' % (self.username, self.first_name, self.last_name)

	def get_short_name(self):
		"""
			Retrieves the short name for the user
		"""
		return str(self.username)

	def get_group_permissions(self, obj=None):
		"""
			Returns a list of permission strings that this user has through their
			groups. This method queries all available auth backends. If an object
			is passed in, only permissions matching this object are returned.
		"""
		permissions = set()
		for backend in auth.get_backends():
			if hasattr(backend, "get_group_permissions"):
				permissions.update(backend.get_group_permissions(self, obj))
		return permissions

	def get_all_permissions(self, obj=None):
		"""
			Get all permissions
		"""
		return _user_get_permissions(self, obj,from_name=None)

	def has_perm(self, perm, obj=None):
		"""
			Returns True if the user has the specified permission. This method
			queries all available auth backends, but returns immediately if any
			backend returns True. Thus, a user who has permission from a single
			auth backend is assumed to have permission in general. If an object is
			provided, permissions for this specific object are checked.
		"""

		# Active superusers have all permissions.
		if self.is_active and self.is_superuser:
			return True

		# Otherwise we need to check the backends.
		return _user_has_perm(self, perm, obj)

	def has_perms(self, perm_list, obj=None):
		"""
			Returns True if the user has each of the specified permissions. If
			object is passed, it checks if the user has all required perms for this
			object.
		"""
		return all(self.has_perm(perm, obj) for perm in perm_list)

	def has_module_perms(self, app_label):
		"""
			Returns True if the user has any permissions in the given app label.
			Uses pretty much the same logic as has_perm, above.
		"""
		# Active superusers have all permissions.
		if self.is_active and self.is_superuser:
			return True

		return _user_has_module_perms(self, app_label)

	class Meta(BaseModel.Meta):
		unique_together = ('id',)


class ExtendedSUserPermission(BaseModel):
	"""
	This model manages the extended users permissions,
	"""
	SUser = models.ForeignKey(SUser, on_delete=models.CASCADE)
	permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '%s %s' % (self.SUser, self.permission.name)

	class Meta(object):
		unique_together = ('SUser', 'permission')
		verbose_name = 'Extended Permission'
		verbose_name_plural = 'Extended Permissions'
