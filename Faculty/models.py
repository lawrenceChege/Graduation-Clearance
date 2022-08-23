from django.db import models

from base.models import BaseModel, GenericBaseModel, State
from system_users.models import SUser

class Programme(GenericBaseModel):
    """
	Defines the Levels : Masters, Degree, certificate
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)


class Faculty(GenericBaseModel):
    """
	Defines the Differnt Schools
	"""
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class Department(GenericBaseModel):
    """
	Defines the Differnt departments with a school
	"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class HeadOfDepartment(BaseModel):
    """
	Defines the head of a department
	"""
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    head = models.ForeignKey(SUser, on_delete=models.CASCADE)
    status = models.ForeignKey(State, on_delete=models.CASCADE)
	

class Course(GenericBaseModel):
    """
    Defines the different courses
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Programme, on_delete=models.CASCADE)
    program_goal = models.TextField(blank=True, null=True)
    no_of_years = models.IntegerField(default=0)
    no_of_semesters = models.IntegerField(default=0)
    minimum_requirement = models.TextField(blank=True, null=True)
    fees = models.DecimalField(default=0.00, decimal_places=2, max_digits=25)


class Unit(GenericBaseModel):
    """
    Defines the different units
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
