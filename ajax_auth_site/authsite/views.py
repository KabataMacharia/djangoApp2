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
        uform = UserForm(data=request.POST)
        pform = UserProfileForm(data = request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            pw = user.password
            user.set_password(pw)
            user.save()
            profile = pform.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(uform.errors, pform.errors)
    else:
        uform = UserForm()
        pform = UserProfileForm()        
    return render(request, 'authsite/register.html', {'uform': uform, 'pform': pform, 'registered': registered })

 
def user_login(request):    
    response_data = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        global userobj
        userobj = authenticate(username=username, password=password)
        if userobj is not None:
            if userobj.is_active:                
                login(request,userobj) 
                global logging_in
                logging_in=userobj.username  
                logout(request)             
                response_data['logging_in']=logging_in
                print("logging_in: ",logging_in) 
                uname=UserProfile.objects.filter(user__username=logging_in)
                sms_number = uname[0].phone_number
                print("sending verification code to:",sms_number)
                print("Verify Code",verify_code)
                messaging = MessagingClient(customer_id, api_key)
                response = messaging.message(sms_number, message, message_type)
                if verified != True:
                    logout(request)
                          
                      
                return JsonResponse(response_data)
            else:                
                return HttpResponse("Your account is disabled")
                
        else:            
            #return 'invalid login eorror'
            print("Invalid login details "+username+" "+password)
            return render(request,'authsite/login.html', {})
    else:        
        #login now leads to login.html
        return render(request,'authsite/login.html',{})
        
@csrf_exempt
def code_verify(request):
    #logging_in = None
    response_data = {}    
    
    #if request.user.is_authenticated():
        #logging_in = request.user.username
    print("logging_in: ",logging_in)
    if request.method == 'POST':
        code = request.POST.get('code')
        response_data = {}
        response_data['code'] = code        
        uname=UserProfile.objects.filter(user__username=logging_in)
            
    if (verify_code == code.strip()):
        response_data['verified_user'] = 'True'
        global verified
        verified = True 
        login(request,userobj)
    else:
        logout(request)
    
    return JsonResponse(response_data)

    
@login_required
def restricted(request):
    return HttpResponse('Authsite says: since you are an authenticated user you can view this restricted page.')

def user_logout(request):    
    logout(request)
    #Go back to index:
    return redirect('/login')

    
