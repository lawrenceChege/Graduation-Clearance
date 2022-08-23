from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.
def add_programme(request):
    return HTTPResponse("Programme added")

def update_programme(request):
    return HTTPResponse("Programme updated")

def view_programme(request):
    return HTTPResponse("Programme")

def view_all_programmes(request):
    return HTTPResponse("All Programmes")

def add_faculty(request):
    return HTTPResponse("faculty added")

def update_faculty(request):
    return HTTPResponse("faculty updated")

def view_faculty(request):
    return HTTPResponse("faculty")

def view_all_faculties(request):
    return HTTPResponse("All faculties")

def add_department(request):
    return HTTPResponse("department added")

def update_department(request):
    return HTTPResponse("department updated")

def view_department(request):
    return HTTPResponse("department")

def view_all_departments(request):
    return HTTPResponse("All departments")

def add_hod(request):
    return HTTPResponse("hod added")

def update_hod(request):
    return HTTPResponse("hod updated")

def view_hod(request):
    return HTTPResponse("hod")

def view_all_hods(request):
    return HTTPResponse("All hods")

def add_course(request):
    return HTTPResponse("course added")

def update_course(request):
    return HTTPResponse("course updated")

def view_course(request):
    return HTTPResponse("course")

def view_all_courses(request):
    return HTTPResponse("All courses")

def add_unit(request):
    return HTTPResponse("unit added")

def update_unit(request):
    return HTTPResponse("unit updated")

def view_unit(request):
    return HTTPResponse("unit")

def view_all_units(request):
    return HTTPResponse("All units")