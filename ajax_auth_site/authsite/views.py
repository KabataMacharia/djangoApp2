from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from authsite.models import *
from authsite.forms import *
#for class-based views:
from django.views.generic import TemplateView
#Twilio Authy
#pip install authy
from authy.api import AuthyApiClient

import json
from django.utils.html import strip_tags

#Authy Account Variables
AUTHY_KEY = 'AxGVrFbD6MDwKUvPt43G2nvihFgZBxPU'
authy_api = AuthyApiClient(AUTHY_KEY)

verified=False
logging_in=None
userobj=None


class RegisterView(View):
    template_name = 'authsite/register.html'
    form_class = UserForm
    uform =  UserForm()
    registered = False 
    print("We are in RegisterView")

    def post(self, request, *args, **kwargs):      
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
            #authy_user = authy_api.users.create(cleaned_email, cleaned_phone_number, 254)
            #if authy_user.ok():
                #user.authy_id = authy_user.id 
            
            user.save()  
            self.registered = True
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
    
    
    def get(self, request, *args, **kwargs):
        #uform = UserForm() 
        #self.registered = False
        return render(request, 'authsite/register.html', {'uform': self.uform, 'registered': self.registered })
    

class UserLoginView(View):
    template_name = 'authsite/login.html'
    form_class = LoginForm
    initial = {'lform': LoginForm()}     
    print("We are in UserLoginView")
    admin = False
    staff = False
    superuser = False

    def post(self, request, *args, **kwargs):  
        print("This is post")  
        response_data = {}    
        #Perform validation and clean on login form, instead of using request.POST[username]"
        lform = LoginForm(data=request.POST)
        #print
        print("Lform",lform)        
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
                #authy_id = uname[0].authy_id
                #sms = authy_api.users.request_sms(authy_id)                
                
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
            
        return render(request, self.template_name, self.initial)
     


    def get(self, request, *args, **kwargs): 
        print("We're in def get")
        lform = LoginForm(data=request.GET)
        print("LFORM GET 1",lform)
        #lform
        try:
            code = request.GET['code']        
            user_entered_verifycode = code
            print('CODE GET IS:',code)
            response_data = {}
            #richie edit            
            print('self.superuser is:',self.superuser )
            
            #authy verfication:
            uname=User.objects.filter(username=logging_in)
            #authy_id = uname[0].authy_id
            #verification = authy_api.tokens.verify(authy_id, user_entered_verifycode, {"force": True})
            
            #authy
            #if verification.ok(): 
            if True:                       
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
                    UserLoginView.admin = True
                if staff:
                    response_data['staff'] = 'True'
                    UserLoginView.staff = True
                if superuser:
                    response_data['superuser'] = 'True'
                    UserLoginView.superuser = True
                    print("self.superuser is now:",UserLoginView.superuser)
                                        
                return JsonResponse(response_data)
            else:
                logout(request)
                return render(request, self.template_name ,self.initial)  
                    
        except:
            #WE have no code in our GET
            print("We are in except")
            #Richie Edit            
            print('UserLoginView.superuser is:',UserLoginView.superuser )
            lform = LoginForm()                                   
            return render(request, self.template_name, self.initial)
        
        print("We are out of try/except blocks")        
        return render(request, self.template_name, self.initial)    
    
        
class UserLogoutView(View):    
         #template_name = 'authsite/login.html'                  
    def get(self, request, *args, **kwargs):    
        logout(request)
        UserLoginView.admin = False
        UserLoginView.staff = False
        UserLoginView.superuser = False    
        return redirect('/login')

class SuperUserView(View):    
    def get(self, request, *args, **kwargs):
        print('At class SuperUserView is:',UserLoginView.superuser )           
    
        if(UserLoginView.superuser):        
            template_name = 'authsite/superuser.html'
            print("We are open! at superuser")
        else:
            print("We are unauth at superuser")
            template_name = 'authsite/unauth.html'
        
        return render(request, template_name)    
        
    
class AdminsView(View):
    def get(self, request, *args, **kwargs):
        print('At class AdminsView is:',UserLoginView.admin )           
    
        if(UserLoginView.admin):        
            template_name = 'authsite/admin.html'
            print("We are open! at admins")
        else:
            print("We are unauth at admins")
            template_name = 'authsite/unauth.html'
        
        return render(request, template_name)

class StaffView(View):
    def get(self, request, *args, **kwargs):
        print('At class StaffView is:',UserLoginView.staff )           
    
        if(UserLoginView.staff):        
            template_name = 'authsite/staff.html'
            print("We are open! at staff")
        else:
            print("We are unauth at staff")
            template_name = 'authsite/unauth.html'
        
        return render(request, template_name)

class UnauthView(TemplateView):
    template_name = 'authsite/unauth.html'
    
class UserHomeView(View):
    def get(self, request, *args, **kwargs):
        if (UserLoginView.staff or UserLoginView.superuser):            
            return redirect('/login')
        else: 
            template_name = 'authsite/userhome.html'
            return render(request, template_name)

        
class AdminHomeView(TemplateView):
    template_name = 'authsite/admin_home.html'

    
