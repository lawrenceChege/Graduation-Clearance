from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.
def add_result_slip(request):
    return HTTPResponse("result_slip added")

def update_result_slip(request):
    return HTTPResponse("result_slip updated")

def view_result_slip(request):
    return HTTPResponse("result_slip")

def view_all_result_slips(request):
    return HTTPResponse("All result_slips")

def add_certificate(request):
    return HTTPResponse("certificate added")

def update_certificate(request):
    return HTTPResponse("certificate updated")

def view_certificate(request):
    return HTTPResponse("certificate")

def view_all_certificates(request):
    return HTTPResponse("All certificates")

