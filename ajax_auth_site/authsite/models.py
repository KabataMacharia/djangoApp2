from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.
        
#models and respective forms for signup and login 
     
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.user.username
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password",)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number"]
