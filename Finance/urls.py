from django.urls import path

from . import views

urlpatterns = [
    # ex: /store/
    path('', views.view_all_student_fee_payments, name='all student fee payments'),
    path('student_fee_payment/add', views.add_student_fee_payment, name='new student_fee_payment'),
    path('student_fee_payment/view', views.view_student_fee_payment, name='show student_fee_payment'),
    path('student_fee_payment/update', views.update_student_fee_payment, name='update student_fee_payment'),
    path('student_fee/all', views.view_all_student_fees, name='all student_fees'),
    path('student_fee/add', views.add_student_fee, name='new student_fee'),
    path('student_fee/view', views.view_student_fee, name='show student_fee'),
    path('student_fee/update', views.update_student_fee, name='update student_fee'),
    path('fee/all', views.view_all_fees, name='all fees'),
    path('fee/add', views.add_fee, name='new fee'),
    path('fee/view', views.view_fee, name='show fee'),
    path('fee/update', views.update_fee, name='update fee'),
]