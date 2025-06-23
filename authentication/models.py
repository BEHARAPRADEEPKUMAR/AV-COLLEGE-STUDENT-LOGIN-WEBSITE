from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # Import the manager

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# class CustomUser(AbstractUser):
    
#     rollno = models.CharField(max_length=20, unique=True)
#     dateofbirth = models.DateField(null=True, blank=True)
#     email = models.EmailField(unique=True)
#     photo = models.ImageField(upload_to='images/', blank=True, null=True)
#     group = models.CharField(max_length=100)
#     achievements = models.TextField(blank=True, null=True)

#     USERNAME_FIELD = 'rollno'  # Set roll number as the unique identifier
#     REQUIRED_FIELDS = ['email', 'dateofbirth']

#     objects = CustomUserManager()  # Use the custom manager

#     def __str__(self):
#         return self.rollno

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
class CustomUserManager(BaseUserManager):
    def create_user(self, rollno, email, password=None, **extra_fields):
        if not rollno:
            raise ValueError("The Roll Number must be set")
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(rollno=rollno, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rollno, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(rollno, email, password, **extra_fields)


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     fname = models.CharField(max_length=20, default="Default Name")  # Adjust as needed
#     lname = models.CharField(max_length=20, default="Default LastName")

#     rollno = models.CharField(max_length=20, unique=True)
#     dateofbirth = models.DateField(null=True, blank=True)
#     group = models.CharField(max_length=50, blank=True, null=True)
#     achievements = models.TextField(blank=True, null=True)
#     photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

#     # Required Fields
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['fname', 'lname', 'rollno']

#     def __str__(self):
#         return self.email

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=20, default="Default Name")  
    lname = models.CharField(max_length=20, default="Default LastName")
    rollno = models.CharField(max_length=20, unique=True)  # Unique Roll Number
    dateofbirth = models.DateField(null=True, blank=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    # Use rollno for login
    USERNAME_FIELD = 'rollno'
    REQUIRED_FIELDS = ['email', 'fname', 'lname']

    def __str__(self):
        return self.rollno

    
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csproject.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
