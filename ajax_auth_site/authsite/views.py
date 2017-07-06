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
#2fa
#from telesign.api import Verify

from django.utils.html import strip_tags

#telesign account variables
customer_id = "1A160C03-C778-4193-B6B0-FD34DC02F357"
api_key = "bszbKGzRVzdUP66AGw+De/Dp9NHItRS5/X2RvmRMjqQJ4mBAYfiiSrN9R1SFRVUyNK+53GcebNBwoEqjbMUSPQ=="
#secret_key = "bszbKGzRVzdUP66AGw+De/Dp9NHItRS5/X2RvmRMjqQJ4mBAYfiiSrN9R1SFRVUyNK+53GcebNBwoEqjbMUSPQ=="
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
            
            #error string formatting
            specific_error = my_error.replace('<ul class="errorlist">',' : ')
            specific_error = strip_tags(specific_error)
            specific_error = specific_error.replace('.','\n')
            specific_error = specific_error.replace(' : ','',1)
            print(specific_error)
            
            response_data['specific_error'] = specific_error           
            return JsonResponse(response_data)
    else:
        uform = UserForm()              
    return render(request, 'authsite/register.html', {'uform': uform, 'registered': registered })

 
def user_login(request):    
    response_data = {}    
    if request.method == 'POST':
        #Perform validation and clean on login form, instead of using request.POST[username]"
        lform = LoginForm(data=request.POST)
        print("LFORM",lform)        
        username = lform.clean_username()
        password = lform.clean_password()
        
        
        if (type(username) == dict):
            uform.add_error(None,username)
        
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
                #2fa
                #user_verification = Verify(customer_id, secret_key)
                #phone_info = user_verification.sms(sms_number, use_case_code="ATCK")
                #status_info = user_verification.status(phone_info.data["reference_id"],verify_code=user_entered_verifycode)
                #print("2FA, STATUS:",status_info.data["verify"]["code_state"])
                
                #If they don't correctly enter code, log them out instantly
                if verified != True:
                    logout(request)
                return JsonResponse(response_data)
            else:                
                return HttpResponse("Your account is disabled")
                
        else:            
            #return 'invalid login error' and redirect to login page
            print("Invalid login details "+username+" "+password)
            return render(request,'authsite/login.html', {'lform': lform})
     
    #Get the SMS code they've submitted
    else:
        lform = LoginForm(data=request.GET)
        print("LFORM GET",lform)
        try:
            code = request.GET['code'] 
            #code = clean_sms_code(code)
            #2fa
            #user_entered_verifycode = code
            #response_data = {}             
            
            print('CODE GET IS:',code)
            response_data = {}
             
            #2fa
            #print("2FA, STATUS AFTER SUBMIT:",status_info.data["verify"]["code_state"])
            #if status_info.data["verify"]["code_state"] == 'VALID':
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
                return render(request,'authsite/login.html',{'lform': lform})
                
        except:
            #WE have no code in our GET
            lform = LoginForm()                                   
            return render(request,'authsite/login.html',{'lform': lform})
                       

@login_required
def restricted(request):
    return HttpResponse('Authsite says: since you are an authenticated user you can view this restricted page.')

def user_logout(request):    
    logout(request)
    #Go back to index:
    return redirect('/login')

    
