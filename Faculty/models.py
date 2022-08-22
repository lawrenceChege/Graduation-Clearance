from pyexpat import model
from sre_constants import GROUPREF_EXISTS
from telnetlib import STATUS
from tkinter import CASCADE
from typing import Tuple
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
    faculty = models.ForeignKey(Faculty, on_delete=CASCADE)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class HeadOfDepartment(BaseModel):
    """
	Defines the head of a department
	"""
    department = models.ForeignKey(Department, on_delete=CASCADE)
    head = models.ForeignKey(SUser, on_delete=models.CASCADE)
    status = models.ForeignKey(State, on_delete=models.CASCADE)
	

class Course(GenericBaseModel):
    """
    Defines the different courses
    """
    department = models.ForeignKey(Department, on_delete=CASCADE)
    level = models.ForeignKey(Programme, on_delete=CASCADE)
    program_goal = models.TextField(blank=True, null=True)
    no_of_years = models.IntegerField(default=0, max_length=2)
    no_of_semesters = models.IntegerField(default=0, max_length=2)
    minimum_requirement = models.TextField(blank=True, null=True)
    fees = models.DecimalField(default=0.00, max_digits=25)


class Unit(GenericBaseModel):
    """
    Defines the different units
    """
    course = models.ForeignKey(Course, on_delete=CASCADE)
