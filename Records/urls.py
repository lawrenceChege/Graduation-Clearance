from django.urls import path

from . import views

urlpatterns = [
    # ex: /store/
    path('', views.view_all_certificates, name='all certificate'),
    path('certificate/add', views.add_certificate, name='new certificate'),
    path('certificate/view', views.view_certificate, name='show certificate'),
    path('certificate/update', views.update_certificate, name='update certificate'),
    path('result_slip/all', views.view_all_result_slips, name='all result slips'),
    path('result_slip/add', views.add_result_slip, name='new result_slip'),
    path('result_slip/view', views.view_result_slip, name='show result_slip'),
    path('result_slip/update', views.update_result_slip, name='update result_slip'),
]