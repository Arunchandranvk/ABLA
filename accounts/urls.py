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
    path('requested_added_by_user/<int:pk>/',UserRequest_FacultyView.as_view(),name='reqed'),
    path('all_requests/',UserRequestGETView.as_view(),name='All_req'),
    path('faculty_accept_request/<int:pk>/',Faculty_Request_AcceptView.as_view(),name='reqaccept_faculty'),
    path('faculty_reject_request/<int:pk>/',Faculty_Request_RejectView.as_view(),name='reqreject_faculty'),
    path('faculty_videos_add/',Faculty_Videos_add_View.as_view(),name='videos_faculty_add'),
    path('faculty_videos/',Faculty_VideosView.as_view(),name='videos_faculty'),
    path('faculty_meetings_add/',Faculty_Meeting_add_View.as_view(),name='meeting_faculty_add'),
    path('faculty_meetings/',Faculty_MeetingsView.as_view(),name='meeting_faculty'),
    path('faculty_by_category/<int:pk>/',CategoryWiseFacultyView.as_view(),name='faculty'),
]