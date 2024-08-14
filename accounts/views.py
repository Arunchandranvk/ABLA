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
    def get(self,request,args,*kwargs):
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