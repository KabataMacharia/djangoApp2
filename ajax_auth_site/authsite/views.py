from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from authsite.models import *
from authsite.forms import *

import json
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits

from bs4 import BeautifulSoup
import re

#telesign account variables
customer_id = "1A160C03-C778-4193-B6B0-FD34DC02F357"
api_key = "bszbKGzRVzdUP66AGw+De/Dp9NHItRS5/X2RvmRMjqQJ4mBAYfiiSrN9R1SFRVUyNK+53GcebNBwoEqjbMUSPQ=="
message_type = "OTP"
verify_code = random_with_n_digits(5)
message = "Your code is {}".format(verify_code)
verified=False
logging_in=None
userobj=None



def register(request):    
    registered = False
    
    if request.method == 'POST':
        response_data = {}
        uform = UserForm(data=request.POST) 
        print("UFORM",uform)  
        
        cleaned_email=uform.clean_email()
        cleaned_username=uform.clean_username()
        cleaned_password=uform.clean_password()
        cleaned_phone_number=uform.clean_phone_number()
        
        print(cleaned_username)
        print(cleaned_email)        
        print(cleaned_phone_number)
        print("cleaned_password_response:",cleaned_password)
        
        if (type(cleaned_password) == dict):
            uform.add_error(None,cleaned_password)
        if (type(cleaned_email) == dict):
            uform.add_error(None,cleaned_email)
        if uform.is_valid():
            print("UFORM IS VALID!")
            user = uform.save()
            pw = cleaned_password
            user.set_password(pw)
            user.save()  
            registered = True
            response_data['error_present'] = 'NO' 
            return JsonResponse(response_data)
        else:
            response_data = {}
            response_data['uform_errors'] = uform.errors
            response_data['error_present'] = 'YES'            
            my_error = str(uform.errors)
            
            #strip <li> tags using BeautifulSoup
            specific_error = ' '
            soup = BeautifulSoup(my_error, "html.parser")
            for a in soup.find_all('li'):
                if a != None:
                    for b in a.find_all('li'):
                        x =  BeautifulSoup(str(b)).text                                                                     
                        specific_error += x+'\n'
                        print(specific_error)
                
            response_data['specific_error'] = specific_error             
            return JsonResponse(response_data)
    else:
        uform = UserForm()              
    return render(request, 'authsite/register.html', {'uform': uform, 'registered': registered })

 
def user_login(request):    
    response_data = {}    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']       
        
        #Authenticate our user, but don't complete login yet.
        #Save the User Object for login after two-step completion  
        global userobj
        userobj = authenticate(username=username, password=password)
        if userobj is not None:
            if userobj.is_active:                
                login(request,userobj) 
                global logging_in
                logging_in=userobj.username  
                logout(request)             
                response_data['logging_in']=logging_in
                
                #find out User's number                 
                uname=User.objects.filter(username=logging_in)
                sms_number = uname[0].phone_number
                print("sending verification code to:",sms_number)
                print("Verify Code",verify_code)
                
                #Send verification message once we have authenticated our user
                messaging = MessagingClient(customer_id, api_key)
                response = messaging.message(sms_number, message, message_type)
                
                #If they don't correctly enter code, log them out instantly
                if verified != True:
                    logout(request)
                return JsonResponse(response_data)
            else:                
                return HttpResponse("Your account is disabled")
                
        else:            
            #return 'invalid login error' and redirect to login page
            print("Invalid login details "+username+" "+password)
            return render(request,'authsite/login.html', {})
     
    #Get the SMS code they've submitted
    elif request.method == 'GET':
        #Does the GET message include our code?        
        try:
            code = request.GET['code'] 
            response_data = {}             
            
            print('CODE GET IS:',code)
            response_data = {}
                             
            if (verify_code == code.strip()):
                print("They match")
                response_data['verified_user'] = 'True'
                
                #User has completed two step verification, don't log them out 
                global verified
                verified = True 
                login(request,userobj)
                return JsonResponse(response_data)
            else:
                logout(request)
        except:
            #WE have no code in our GET                        
            return render(request,'authsite/login.html',{})
                       
    else: 
        #Not POST or GET with code       
        #login now leads to login.html
        return render(request,'authsite/login.html',{})
        

@login_required
def restricted(request):
    return HttpResponse('Authsite says: since you are an authenticated user you can view this restricted page.')

def user_logout(request):    
    logout(request)
    #Go back to index:
    return redirect('/login')

    
