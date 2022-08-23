
from django.db import models

from Faculty.models import Course, Unit
from base.models import BaseModel, GenericBaseModel, State
from system_users.models import SUser

# Create 
class Grade(GenericBaseModel):
    """
	Defines the resultslip
	"""
    upper_marks = models.IntegerField(null=True, blank=True)
    lower_marks = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.name, self.upper_marks, self.lower_marks, self.status)

class Distinction(GenericBaseModel):
    """
	Defines the resultslip
	"""
    upper_gpa = models.IntegerField(null=True, blank=True)
    lower_gpa = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.name, self.upper_gpa, self.lower_gpa, self.status)

class ResultSlip(BaseModel):
    """
	Defines the resultslip
	"""
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    marks = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.student, self.course, self.unit, self.grade)


class Certificate(BaseModel):
    """
	Defines the graduation certificate
	"""
    student = models.ForeignKey(SUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    distinction = models.ForeignKey(Distinction, on_delete=models.CASCADE)
    status = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s' % (self.student, self.course, self.distinction, self.status)