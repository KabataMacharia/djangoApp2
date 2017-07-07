from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from authsite.models import *
from authsite.forms import *

#Twilio Authy
from authy.api import AuthyApiClient

import json
from django.utils.html import strip_tags


#Authy Account Variables
AUTHY_KEY = 'AxGVrFbD6MDwKUvPt43G2nvihFgZBxPU'
authy_api = AuthyApiClient(AUTHY_KEY)

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
            print("UFORM",uform)          
            user = uform.save()
            pw = cleaned_password
            user.set_password(pw)
            #create authy_user
            authy_user = authy_api.users.create(cleaned_email, cleaned_phone_number, 254)
            if authy_user.ok():
                user.authy_id = authy_user.id 
            
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
                
                #sending authy_sms:
                authy_id = uname[0].authy_id
                sms = authy_api.users.request_sms(authy_id)                
                
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
            user_entered_verifycode = code
            print('CODE GET IS:',code)
            response_data = {}
            
            #authy verfication:
            uname=User.objects.filter(username=logging_in)
            authy_id = uname[0].authy_id
            verification = authy_api.tokens.verify(authy_id, user_entered_verifycode, {"force": True})
            
            #authy
            if verification.ok():            
                response_data = dict()              
                print("They match")
                response_data['verified_user'] = 'True'                
                uname=User.objects.filter(username=logging_in)                              
                
                #User has completed two step verification, don't log them out 
                global verified
                verified = True 
                login(request,userobj)
                admin = uname[0].is_admin
                staff = uname[0].is_staff
                superuser = uname[0].is_superuser
                
                print("ADMIN:{0}, STAFF:{1}, SUPERUSER:{2}".format(admin,staff,superuser))
                if admin:
                    response_data['admin'] = 'True'
                if staff:
                    response_data['staff'] = 'True'
                if superuser:
                    response_data['superuser'] = 'True'
                                        
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

    
