from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Group,Permission
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _ 
from mapbox_location_field.models import LocationField



class EventManager(BaseUserManager):            
    
    def create_user(self,email,user_name,password,**extra_fields):
        
        if not email:
            raise ValueError(_('You have to provide email address'))
        email=self.normalize_email(email)
        user=self.model(email=email,user_name=user_name,**extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, user_name, password, **extra_fields):
        # Fix the typo here: change extra_fieldys to extra_fields
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # Make sure to pass the 'username' parameter
        return self.create_user(email, user_name, password, **extra_fields)
        
        


    
class newUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name'] # Change 'username' to 'user_name'
    objects = EventManager()

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email or self.user_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

    
class EventCategory(models.Model):
    name=models.CharField(max_length=150,null=True)
    code=models.PositiveIntegerField()
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
class Event(models.Model):
    category=models.ForeignKey(EventCategory,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    uid=models.PositiveIntegerField()
    description = models.TextField()
    venue = models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField()
    location = models.CharField(max_length=255)
    maximum_attendance = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    image=models.ImageField(upload_to='event/')
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('time out', 'Time Out'),
        ('completed', 'Completed'),
        ('cancel', 'Cancel'),
    )
    status = models.CharField(choices=status_choice, max_length=10)
    speaker_name = models.CharField(max_length=120)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return self.title
    
    
    

