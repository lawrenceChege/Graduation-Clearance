from http.client import HTTPResponse
from django.shortcuts import render


def add_gown(request):
    return HTTPResponse("Gown added")

def update_gown(request):
    return HTTPResponse("Gown eddited")

def issue_gown(request):
    return HTTPResponse("Gown issued")

def return_gown(reuest):
    return HTTPResponse("Gown issued")


def gowns_issued(request):
    return HTTPResponse("These are the gowns issued")


def gowns_returned(request):
    return HTTPResponse("These are the gowns returned")

def late_gowns(request):
    return HTTPResponse("These are the late gowns")


# iii. Degree/Diploma Certificates issued.
# iii. Names of students cleared for graduation.
