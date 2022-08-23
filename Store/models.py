
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

    def __str__(self):
        return '%s %s' % (self.size, self.programme)

class BorrowedGown(BaseModel):
    """
	Defines the graduation gown borrowed
	"""
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    gown = models.ForeignKey(GraduationGown, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now=True)
    return_date = models.DateField(auto_now=True)
    penalty = models.DecimalField(max_digits=25, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=25, decimal_places=2,  null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.student, self.borrow_date, self.retrun_date, self.status)

class BorrowedGownPenalty(BaseModel):
    """
	Defines the graduation gown borrowed
	"""
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    gown = models.ForeignKey(GraduationGown, on_delete=models.CASCADE)
    penalty = models.DecimalField(max_digits=25, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=25, decimal_places=2, null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.student, self.penalty, self.status)