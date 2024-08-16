from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Language
        fields='__all__'
        
        
class OTPVerificationSer(serializers.ModelSerializer):
    class Meta:
        model=OTPVerification
        fields =['email']

        
class VerificationSer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    
    
class RegistrationSerStudent(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    usertype = serializers.ReadOnlyField()
    language_title = serializers.ReadOnlyField(source ="language.title")
    class Meta:
        model=CustomUser
        fields=['language','language_title','usertype','name','place','email','password']
        
    def create(self,validated_data):
        return CustomUser.objects.create_user(usertype="Student",**validated_data)
    
    
    
    
class RegistrationFacultySer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    usertype = serializers.ReadOnlyField()
    language_title = serializers.ReadOnlyField(source ="language.title")
    class Meta:
        model=Faculty
        fields=['id','language','category','language_title','usertype','faculty_name','place','email','password','rating','title','certification','experience','price','status']
        
    def create(self,validated_data):
        return Faculty.objects.create_user(usertype="Faculty",**validated_data)
    
    
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            faculty=Faculty.objects.get(id=user.id)
            token['category'] = faculty.category.cat_name
        except Faculty.DoesNotExist:
            pass
        token['name'] = user.name
        token['place'] = user.place
        token['email'] = user.email
        token['usertype'] = user.usertype
        
        try:
            token['language'] = user.language.title
        except:
            token['language'] = user.language
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user=self.user
        try:
            faculty=Faculty.objects.get(id=user.id)
            data['category'] = faculty.category.cat_name
        except Faculty.DoesNotExist:
            pass
        data['name'] = user.name
        data['place'] = user.place
        data['email'] = user.email
        data['usertype'] = user.usertype
        
        try:
            data['language'] = user.language.title
        except:
            data['language'] = user.language
        return data
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class UserRequestSer(serializers.ModelSerializer):
    user=RegistrationSerStudent()
    faculty=RegistrationFacultySer()
    class Meta:
        model = UserRequest
        fields = '__all__'
    
    
class AllRequestSer(serializers.ModelSerializer):
    user =RegistrationSerStudent()
    faculty = RegistrationFacultySer()
    meetings = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    
    class Meta:
        model = UserRequest
        fields = ['id','user','faculty','status','meetings','videos']
        
    def get_meetings(self,obj):
        print( obj.status)
        if obj.status == "Accepted":
            meetings = FacultyMeetings.objects.filter(faculty = obj.faculty)
            return FacultyMeetingsSerializer(meetings,many=True).data
        else:
            pass
    
    def get_videos(self,obj):
        if obj.status == "Accepted":
            video = FacultyVideos.objects.filter(faculty = obj.faculty)
            return  FacultyVideosSerializer(video,many=True).data
        else:
            pass
    
class FacultyMeetingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyMeetings
        fields = '__all__'
    
class FacultyVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyVideos
        fields = '__all__'