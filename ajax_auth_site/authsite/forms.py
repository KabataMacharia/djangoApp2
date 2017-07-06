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
                #print("inside try/catch block!")
                password_validate.validate_password(password=password2)
                return password2
            except exceptions.ValidationError as e:
                errors['password2'] = list(e.messages)                
                for i in range(len(errors['password2'])):
                    if 'short' in errors['password2'][i]:
                        errors['password2'][i] = 'This password is too short, It must contain at least 8 characters!.'
                    else:
                        errors['password2'][i] = 'This password is entirely numeric!.'
                print(errors) 
                return errors             
        else:
            print("Passwords don't match")            
            password_match = False
            errors['password2'] = "Passwords do not match!."
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
            errors['email'] = "Enter a valid email address please!." 
            return errors
        if valid_email:
            return email
            
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            validators.validate_slug(username)
            valid_username = True
        except:
            raise forms.ValidationError("Username is not valid, Special characters used!.")
            valid_username = False
        if valid_username:
            if(User.objects.filter(username=username).exists()):
                print("Sorry, a user with that Username already exists!.")
                raise forms.ValidationError("Sorry, a user with that Username already exists!.")
                return None
            else:
                return username
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        try:
            validators.validate_integer(phone_number)
            valid_phone_number = True
        except:
            raise forms.ValidationError("Not a valid phone number, 0-9 only!.")
            valid_phone_number = False
        if valid_phone_number:
            return phone_number
            
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    sms_code = forms.IntegerField(required=False)
    
    class Meta:
        model = User
        fields = ("username","password","sms_code")
        
    def clean_username(self):
        print("Cleaning username....")
        username = self.cleaned_data.get("username")
        return username
            
    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:            
            print("Cleaning password....")
            valid_password = True
        except:
            raise forms.ValidationError("Check your password input again!.")
            valid_password = False
        if valid_password:
            return password
            
    def clean_sms_code(self):
        sms_code = self.cleaned_data.get("sms_code")
        try:
            print("Cleaning sms code...")
            valid_sms_code = True
        except:
            raise forms.ValidationError("Not a valid sms code, 0-9 only!.")
            valid_sms_code = False
        if valid_sms_code:
            return sms_code
    
        
        
    
