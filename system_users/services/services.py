"""
SUser module services
"""
from base.backend.servicebase import ServiceBase
from system_user.models import SUser, SUserPassword, Role, Permission, RolePermission, ExtendedSUserPermission, \
	SUserSecurityQuestion


class RoleService(ServiceBase):
	"""
	This class handles all the CRUD operations for the Role Model
	"""

	manager = Role.objects


class PermissionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the Permission Model
	"""
	manager = Permission.objects


class RolePermissionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the RolePermission Model
	"""
	manager = RolePermission.objects


class SUserPasswordService(ServiceBase):
	"""
	This class handles all the CRUD operations for the SUserPassword Model
	"""
	manager = SUserPassword.objects


class SUserSecurityQuestionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the SUserSecurityQuestion Model
	"""
	manager = SUserSecurityQuestion.objects


class SUserService(ServiceBase):
	"""
	This class handles all the CRUD operations for the SUser Model.
	"""
	manager = SUser.objects


class ExtendedSUserPermissionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the ExtendedUserPermission Model
	"""
	manager = ExtendedSUserPermission.objects
