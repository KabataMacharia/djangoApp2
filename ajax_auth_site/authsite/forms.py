from django import forms
#from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators




class UserForm(forms.ModelForm):  
    password1 = forms.CharField(widget=forms.TextInput)
    password2 = forms.CharField(widget=forms.TextInput)
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.EmailInput)
    phone_number = forms.IntegerField(validators=[validators.validate_integer])  
     
        
    class Meta:
        model = User 
        #widgets = {
        #'password1': forms.PasswordInput(),
        #'password2': forms.PasswordInput(),        
        #}   
        fields = ("username", "email", "password1", "password2", "phone_number")
        
    #def clean_password2(self):
        ## Check that the two password entries match
        #password1 = self.cleaned_data.get("password1")
        #password2 = self.cleaned_data.get("password2")
        #if password1 != password2:
            #raise forms.ValidationError("Passwords don't match")
            #print("Passwords don't match")
        #else:
            #return password2
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validators.validate_email(email)
            valid_email = True
        except:
            raise forms.ValidationError("Not a valid email address")
            valid_email = False
        if valid_email:
            return email
            
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            validators.validate_slug(username)
            valid_username = True
        except:
            raise forms.ValidationError("Not a valid username. Special characters used")
            valid_username = False
        if valid_username:
            return username
            
        
        
            

    

        

