from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
   
#models for signup and login 

class MyUserManager(BaseUserManager):
        
    def create_superuser(self, username, password, email, phone_number):
        user = self.create_user(username=username, password=password, email=email, phone_number=phone_number)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user
        
    def create_user(self, username, password, email, phone_number, is_superuser, is_admin, is_staff):
        user = self.model(email=self.normalize_email(email),
        username=username, phone_number=phone_number, is_admin=is_admin, is_superuser=is_superuser, is_staff=is_staff)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_active = True
        user.is_admin = is_admin
        user.is_superuser = is_superuser
        user.save (using=self._db) 
        return user  
         

        
class User(AbstractBaseUser):  
    phone_number = models.CharField(max_length=20) 
    username = models.CharField(max_length=20, unique=True) 
    email = models.CharField(max_length=50, blank=True)    
    password = models.CharField(max_length=128)
    authy_id = models.CharField(max_length=20)     
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']
    objects = MyUserManager()    
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    
    class Meta:
        def __str__(self):
            return self.username
            
    
        
        
    
    
    
