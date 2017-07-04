from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm



class UserForm(UserCreationForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number"] 
