from django.urls import path

from . import views

urlpatterns = [
    # ex: /store/
    path('', views.gowns_issued, name='issued gowns'),
    path('returned/', views.gowns_returned, name='retruned gowns'),
    path('late/', views.late_gowns, name='late gowns'),
    path('add/', views.add_gown, name='add gown'),
    path('update/', views.add_gown, name='add gown'),
    path('issue/', views.issue_gown, name='issue gown'),
    path('return/', views.return_gown, name='return gown'),
]