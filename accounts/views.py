from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,parsers
import random
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
# Create your views here.


class LanguageView(APIView):
    def get(self,request):
        try:
            lang=Language.objects.all() 
            ser=LanguageSerializer(lang,many=True)
            print(ser.data)
            return Response(data={"Status":"Success","Msg":"Available Languages....","Languages":ser.data},status=status.HTTP_200_OK)
        except Language.DoesNotExist:
            return Response(data={"Status":"Failed","Msg":"No Languages Available......"},status=status.HTTP_204_NO_CONTENT)
        
class SendOTPView(APIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    @swagger_auto_schema(
        request_body=OTPVerificationSer,
        responses={
            200: openapi.Response('OTP sent successfully!', OTPVerificationSer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=OTPVerificationSer(data=request.data)
        if ser.is_valid():
            ser.save()
            email=ser.validated_data.get('email')
            otp=random.randint(100000,999999)
            user=ser.instance
            user.set_otp(otp)
            subject="ABLA - Verification OTP"
            message=f"Verification OTP - {otp}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email= [email]
            send_mail(
                subject,
                message,
                from_email,
                to_email
            )
            return Response(data={"Status":"Success","Msg":"OTP Send Successfully!!!!"},status=status.HTTP_200_OK)
        else:
            print(ser.errors)
            return Response(data={"Status":"Failed","errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)
        

class VerifyOTPView(APIView):
    @swagger_auto_schema(
        request_body=VerificationSer,
        responses={
            200: openapi.Response('OTP sent successfully!', VerificationSer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=VerificationSer(data=request.data)
        if ser.is_valid():
            email=ser.validated_data.get('email')
            otp=ser.validated_data.get('otp')
            print("otp===",otp)
            try:
                
                verification = OTPVerification.objects.filter(email=email).latest()
                if verification and verification.otp and verification.otp_expiration:
                    print("otp",verification.otp)
                    
                    if verification.otp == otp and verification.otp_expiration > timezone.now():
                        print()
                        print("checked")
                        verification.otp = None
                        verification.otp_expiration = None
                        verification.is_verified = True
                        verification.save()
                return Response(data={"Status":"Success","Msg":"OTP Verified!!!","Email":verification.email},status=status.HTTP_200_OK)
            except OTPVerification.DoesNotExist:
                return Response(data={"Status":"Failed","Msg":"Email invalid or OTP Expired!!"},status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            return Response(data={"Status":"Failed","Msg": "Please Enter OTP!!!"}, status=status.HTTP_404_NOT_FOUND)    


class RegistrationStudentView(APIView):
    @swagger_auto_schema(
        request_body=RegistrationSerStudent,    
        responses={
            200:openapi.Response('Registration Successfull...',RegistrationSerStudent),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=RegistrationSerStudent(data=request.data)
        if ser.is_valid():
            try:
                email=ser.validated_data.get('email')
                verify_email=OTPVerification.objects.filter(email=email).latest()
                print(verify_email)
                if verify_email and verify_email.is_verified:
                    ser.save()
                    return Response(data={"Status": "Success", "Msg": "Registration Successful!!!!", "data": ser.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response(data={"Status": "Failed", "Msg": "Email is not verified or does not exist."}, status=status.HTTP_401_UNAUTHORIZED)
            except OTPVerification.DoesNotExist:
                return Response(data={"Status":"Failed","Msg":"Email is Not Verified...."},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"Status":"Failed","Msg":"Registration Unsuccessfull....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
        
     

class RegistrationFacultyView(APIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    @swagger_auto_schema(
        request_body=RegistrationFacultySer,    
        responses={
            200:openapi.Response('Registration Successfull...',RegistrationFacultySer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=RegistrationFacultySer(data=request.data)
        if ser.is_valid():
            try:
                email=ser.validated_data.get('email')
                verify_email=OTPVerification.objects.filter(email=email).latest()
                if verify_email.is_verified:
                    ser.save()
                    return Response(data={"Status":"Success","Msg":"Registration Successfull!!!","data":ser.data},status=status.HTTP_201_CREATED)
            except OTPVerification.DoesNotExist:
                return Response(data={"Status":"Failed","Msg":"Email is Not Verified...."},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"Status":"Failed","Msg":"Registration Unsuccessfull....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
        
        
class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            print(serializer)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            data['Status'] = 'Success'
            return Response(data={"Msg":"Login Success!!!","data":data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response(data={'Status': 'Failed', 'Msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
class CategoryView(APIView):
    def get(self,request):
        try:
            cat = Category.objects.all()
            ser = CategorySerializer(cat,many=True)
            return Response(data={"Status":"Success","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)


class FacultiesView(APIView):
    def get(self,request):
        try:
            faculty = Faculty.objects.filter(status=True)
            ser=RegistrationFacultySer(faculty,many=True)
            return Response(data={"Status":"Success","Msg":"All Faculties Details!!!","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)
        

class UserRequest_FacultyView(APIView):
    def get(self,request,pk):
        try:
            user_id=request.user.id
            user=CustomUser.objects.get(id=user_id)
            print(user)
            faculty = Faculty.objects.get(id=pk)
            print(faculty)
            data=UserRequest.objects.get(user=user,faculty=faculty)
                
            ser=UserRequestSer(data)
            return Response(data={"Status":"Failed","Msg":"User Already Exist!!!!","data":ser.data})
        except UserRequest.DoesNotExist:
            req,created=UserRequest.objects.get_or_create(user=user,faculty=faculty,status="Pending")

            print("created")
            ser=UserRequestSer(req)
            return Response(data={"Status":"Success","Msg":"Request Details!!!","data":ser.data},status=status.HTTP_200_OK)

class UserRequestGETView(APIView):
    def get(self,request):
        try:
            user_id=request.user.id
            user=CustomUser.objects.get(id=user_id)
            req=UserRequest.objects.filter(user=user)
            faculties_accepted = []
            faculty_meetings = []
            faculty_videos = []
            for requests in req:
                if requests.status == "Accepted":
                    faculties_accepted.append(requests.faculty.id)
            print(faculties_accepted)
            for details in faculties_accepted:
                print(details)
                meetings=FacultyMeetings.objects.filter(faculty=details)
                for i in meetings:
                    faculty_meetings.append(i)
                videos=FacultyVideos.objects.filter(faculty=details)
                for j in videos:
                    faculty_videos.append(j)
            print(faculty_videos)
            print(faculty_meetings)
            meetings=FacultyMeetingsSerializer(faculty_meetings,many=True)
            videos=FacultyVideosSerializer(faculty_videos,many=True)
            ser=UserRequestSer(req,many=True)
            return Response(data={"Status":"Success","Msg":"User Request See Here...!!!","data":ser.data,"Meetings":meetings.data,"Videos":videos.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)


class Faculty_Request_AcceptView(APIView):
    def get(self,request,pk):
        try:
            request = UserRequest.objects.get(id=pk)
            request.status = "Accept"
            request.save()
            ser=UserRequestSer(request)
            return Response(data={"Status":"Success","Msg":"Request Accepted  !!!","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)

class Faculty_Request_RejectView(APIView):
    def get(self,request,pk):
        try:
            request = UserRequest.objects.get(id=pk)
            request.status = "Rejected"
            request.save()
            ser=UserRequestSer(request)
            return Response(data={"Status":"Success","Msg":"Request Rejected !!!","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)


class Faculty_MeetingsView(APIView):
    def get(self,request):
        try:
            user_id=request.user.id
            faculty=Faculty.objects.get(id=user_id)
            meetings=FacultyMeetings.objects.filter(faculty=faculty)
            ser=FacultyMeetingsSerializer(meetings,many=True)
            return Response({"Msg":"My Meetings.........","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Msg":"Something Went Wrong!!!!","Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class Faculty_VideosView(APIView):
    def get(self,request):
        try:
            user_id=request.user.id
            faculty=Faculty.objects.get(id=user_id)
            videos=FacultyVideos.objects.filter(faculty=faculty)
            ser=FacultyVideosSerializer(videos,many=True)
            return Response({"Msg":"My Videos.........","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Msg":"Something Went Wrong!!!!","Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        

class Faculty_Meeting_add_View(APIView):
    @swagger_auto_schema(
        request_body=FacultyMeetingsSerializer,    
        responses={
            200:openapi.Response('Meetings Add Successfull...',FacultyMeetingsSerializer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=FacultyMeetingsSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(data={"Status":"Success","Msg":"Meetings Added  Successfull!!!","data":ser.data},status=status.HTTP_201_CREATED)
        else:
            return Response(data={"Status":"Failed","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
       
        
class Faculty_Videos_add_View(APIView):
    @swagger_auto_schema(
        request_body=FacultyVideosSerializer,    
        responses={
            200:openapi.Response('Meetings Add Successfull...',FacultyVideosSerializer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=FacultyVideosSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(data={"Status":"Success","Msg":"Meetings Added  Successfull!!!","data":ser.data},status=status.HTTP_201_CREATED)
        else:
            return Response(data={"Status":"Failed","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  

