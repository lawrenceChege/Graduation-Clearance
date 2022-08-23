from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.
def add_fee(request):
    return HTTPResponse("fee added")

def update_fee(request):
    return HTTPResponse("fee updated")

def view_fee(request):
    return HTTPResponse("fee")

def view_all_fees(request):
    return HTTPResponse("all fees")

def add_student_fee(request):
    return HTTPResponse("student_fee added")

def update_student_fee(request):
    return HTTPResponse("student_fee updated")

def view_student_fee(request):
    return HTTPResponse("student_fee")

def view_all_student_fees(request):
    return HTTPResponse("All student_fees")

def add_student_fee_payment(request):
    return HTTPResponse("student_fee_payment added")

def update_student_fee_payment(request):
    return HTTPResponse("student_fee_payment updated")

def view_student_fee_payment(request):
    return HTTPResponse("student_fee_payment")

def view_all_student_fee_payments(request):
    return HTTPResponse("All student_fee_payments")