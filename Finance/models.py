from tkinter import CASCADE
from django.db import models

from base.models import BaseModel, GenericBaseModel, State

class Fee(GenericBaseModel):
    """
	Defines the different fees: School fee, Graduation fee, library fee
	"""
    amount = models.DecimalField(default=0.00, max_digits=25)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

class StudentFee(BaseModel):
    """
    Defines fees for students
    """
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(default=0.00, max_digits=25)
    balance = models.DecimalField(default=0.00, max_digits=25)

class StudentFeePayment(BaseModel):
    """
    Defines individual payment
    """
    student_fee = models.ForeignKey(StudentFee, on_delete=CASCADE)
    amount = models.DecimalField(default=0.00, max_digits=25)
    receipt = models.TextField(max_length=50, null=True, blank=True)
    

