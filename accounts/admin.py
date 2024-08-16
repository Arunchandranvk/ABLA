from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(OTPVerification)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(UserRequest)
admin.site.register(Faculty)
admin.site.register(FacultyMeetings)
admin.site.register(FacultyVideos)