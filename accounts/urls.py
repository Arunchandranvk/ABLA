from django.urls import path
from .views import *

urlpatterns = [
    path('languages/',LanguageView.as_view(),name='lang'),
    path('email_submit/',SendOTPView.as_view(),name='submitemail'),
    path('verifyotp/',VerifyOTPView.as_view(),name='verift_otp'),
    path('student_registration/',RegistrationStudentView.as_view(),name='reg_stu'),
    path('faculty_registration/',RegistrationFacultyView.as_view(),name='reg_fac'),
    path('login/',LoginView.as_view(),name='log'),
    path('categories/',CategoryView.as_view(),name='cat'),
    path('faculties/',FacultiesView.as_view(),name='faculties'),
]