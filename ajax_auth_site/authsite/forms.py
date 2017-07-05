from django import forms
from .models import User
from django.core import validators
import django.contrib.auth.password_validation as password_validate
from django.core import exceptions




class UserForm(forms.ModelForm):  
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.EmailInput)
    phone_number = forms.IntegerField()  
     
        
    class Meta:
        model = User 
        fields = ("username", "email", "password1", "password2","phone_number")
        
    def clean_password(self):
        # Check that the two password entries match
        print("clean_password called")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        password_match = False
        errors=dict()
        
        if password1 == password2:
            password_match = True
            print("Passwords match")            
            #Passwords match, so validate password 
            try:                
                print("inside try/catch block!")
                password_validate.validate_password(password=password2)
                return password2
            except exceptions.ValidationError as e:
                errors['password2'] = list(e.messages)                
                print(errors) 
                return errors             
        else:
            print("Passwords don't match")            
            password_match = False
            errors['password2'] = "Passwords don't match"
            return errors       
            
    def clean_email(self):
        email = self.cleaned_data.get("email")
        errors=dict()
        valid_email = False
        
        try:
            validators.validate_email(email)
            valid_email = True                            
        except:
            valid_email = False             
            errors['email'] = "Enter a valid email address please" 
            return errors
        if valid_email:
            return email
            
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            validators.validate_slug(username)
            valid_username = True
        except:
            raise forms.ValidationError("Username is not valid. Special characters used")
            valid_username = False
        if valid_username:
            if(User.objects.filter(username=username).exists()):
                print("Sorry, that Username exists.")
                raise forms.ValidationError("Sorry, that Username exists.")
                return None
            else:
                return username
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        try:
            validators.validate_integer(phone_number)
            valid_phone_number = True
        except:
            raise forms.ValidationError("Not a valid phone number. 0-9 only")
            valid_phone_number = False
        if valid_phone_number:
            return phone_number
