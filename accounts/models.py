from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import timedelta
from django.utils import timezone

# Create your models here.


class Language(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)

    def _str_(self):
        return self.title


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    place = models.CharField(max_length=100)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name='languages_user', null=True)
    options = (
        ('Student', 'Student'),
        ('Faculty', 'Faculty')
    )
    usertype = models.CharField(
        max_length=100, choices=options, default="Student")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'place']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def _str_(self):
        return self.email



class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    cat_img = models.FileField(upload_to="Category Images")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def _str_(self):
        return self.cat_name

class Faculty(CustomUser):
    faculty_name = models.CharField(max_length=100)
    rating = models.FloatField()
    title = models.CharField(max_length=200)
    certification = models.FileField(upload_to="faculty_certificate")
    experience = models.CharField(max_length=200)
    price = models.BigIntegerField()
    status = models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="faculty_cat",null=True)

    def _str_(self):
        return self.name


class OTPVerification(models.Model):
    email = models.EmailField(null=True)
    otp = models.CharField(max_length=6, null=True, blank=True, unique=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        get_latest_by = 'created_at'

    def _str_(self):
        return self.email

    def set_otp(self, otp):
        self.otp = otp
        self.otp_expiration = timezone.now() + timedelta(minutes=5)
        self.save()

    def verify_otp(self, otp):
        if self.otp and self.otp_expiration:
            if self.otp == otp and self.otp_expiration > timezone.now():
                self.otp = None
                self.otp_expiration = None
                self.is_verified = True
                self.save()
                return True
        return False

        
        
class UserRequest(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="userrequest_user")
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name="userrequest_faculty")
    options=(
        ("Accepted","Accepted"),
        ("Rejected","Rejected"),
        ("Pending","Pending"),
    )
    status=models.CharField(max_length=100,choices=options)
    

class FacultyMeetings(models.Model):
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name="faculty_meetings")
    meeting_title = models.CharField(max_length=200)
    meeting_link = models.CharField(max_length=500)
    
    def __str__(self):
        return self.meeting_title

class FacultyVideos(models.Model):
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name="faculty_videos")
    video_title = models.CharField(max_length=200)
    video_link = models.CharField(max_length=500)
    
    def __str__(self):
        return self.video_title