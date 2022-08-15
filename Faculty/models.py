from pyexpat import model
from sre_constants import GROUPREF_EXISTS
from telnetlib import STATUS
from tkinter import CASCADE
from typing import Tuple
from django.db import models

from base.models import GenericBaseModel, State

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
	

class Course(GenericBaseModel):
    """
    Defines the different courses
    """
    school = models.ForeignKey(Faculty, on_delete=CASCADE)
    level = models.ForeignKey(Programme, on_delete=CASCADE)
    program_goal = models.TextField(blank=True, null=True)
    no_of_years = models.IntegerField(default=0, max_length=2)
    no_of_semesters = models.IntegerField(default=0, max_length=2)
    minimum_requirement = models.TextField(blank=True, null=True)
    fees = models.DecimalField(default=0.00, max_digits=25)


