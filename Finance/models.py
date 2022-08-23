
from django.db import models

from base.models import BaseModel, GenericBaseModel, State
from system_users.models import SUser

class Fee(GenericBaseModel):
    """
	Defines the different fees: School fee, Graduation fee, library fee
	"""
    amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=25)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.name, self.amount, self.status)

class StudentFee(BaseModel):
    """
    Defines fees for students
    """
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(default=0.00, decimal_places=2, max_digits=25)
    balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=25)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.student, self.fee, self.amount_paid, self.balance)

class StudentFeePayment(BaseModel):
    """
    Defines individual payment
    """
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=25)
    receipt = models.TextField(max_length=50, null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.student_fee, self.receipt, self.amount, self.status)



