from django.urls import path

from . import views

urlpatterns = [
    # ex: /store/
    path('', views.view_all_faculties, name='all faculties'),
    path('faculty/add', views.add_faculty, name='new faculty'),
    path('faculty/view', views.view_faculty, name='show faculty'),
    path('faculty/update', views.update_faculty, name='update faculty'),
    path('department/all', views.view_all_departments, name='all departments'),
    path('department/add', views.add_department, name='new department'),
    path('department/view', views.view_department, name='show department'),
    path('department/update', views.update_department, name='update department'),
    path('programme/all', views.view_all_programmes, name='all programmes'),
    path('programme/add', views.add_programme, name='new programme'),
    path('programme/view', views.view_programme, name='show programme'),
    path('programme/update', views.update_programme, name='update programme'),
    path('course/all', views.view_all_courses, name='all courses'),
    path('course/add', views.add_course, name='new course'),
    path('course/view', views.view_course, name='show course'),
    path('course/update', views.update_course, name='update course'),
    path('unit/all', views.view_all_units, name='all units'),
    path('unit/add', views.add_unit, name='new unit'),
    path('unit/view', views.view_unit, name='show unit'),
    path('unit/update', views.update_unit, name='update unit'),
    path('hod/all', views.view_all_hods, name='all hods'),
    path('hod/add', views.add_hod, name='new hod'),
    path('hod/view', views.view_hod, name='show hod'),
    path('hod/update', views.update_hod, name='update hod'),
]