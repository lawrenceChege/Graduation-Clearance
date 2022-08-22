
from django.db import models

from Faculty.models import Course, Unit
from base.models import BaseModel, State
from system_users.models import SUser

# Create your models here.

class ResultSlip(BaseModel):
    """
	Defines the resultslip
	"""
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    grade = models.TextField(max_length=2,  null=True, blank=True)
    marks = models.IntegerField(max_length=2, null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class Certificate(BaseModel):
    """
	Defines the graduation certificate
	"""
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    distinction = models.TextField(max_length=20,  null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)