
from django.db import models

from Faculty.models import Course, Programme, Unit
from Finance.models import Fee
from base.models import BaseModel, State
from system_users.models import SUser

# Create your models here.

class GraduationGown(BaseModel):
    """
	Defines the graduation gown
	"""
    purchasing_date = models.DateField(auto_now=True)
    size = models.TextField(max_length=3)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class BorrowedGown(BaseModel):
    """
	Defines the graduation gown borrowed
	"""
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    gown = models.ForeignKey(GraduationGown, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now=True)
    retrun_date = models.DateField(auto_now=True)
    penalty = models.DecimalField(max_length=20,  null=True, blank=True)
    balance = models.DecimalField(max_length=20,  null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)