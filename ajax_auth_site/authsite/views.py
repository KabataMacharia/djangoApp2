from django.shortcuts import render
from django.http import HttpResponse
from authsite.models import Post
from authsite.forms import PostForm

import json
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits

#telesign account variables
customer_id = "1A160C03-C778-4193-B6B0-FD34DC02F357"
api_key = "bszbKGzRVzdUP66AGw+De/Dp9NHItRS5/X2RvmRMjqQJ4mBAYfiiSrN9R1SFRVUyNK+53GcebNBwoEqjbMUSPQ=="
message_type = "OTP"
verify_code = random_with_n_digits(5)
message = "Your code is {}".format(verify_code)
messaging = MessagingClient(customer_id, api_key)


def home(req):

    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'form': PostForm()
    }
    return render(req, 'authsite/index.html', tmpl_vars)

def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post') 
        email_post = request.POST.get("the_email")
        password_post = request.POST.get("the_password")
        response_data = {}

        post = Post(text=post_text, email=email_post, password=password_post, author=request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created
        response_data['author'] = post.author.username      
        
        phone_number=post.text
        #email_post=post.email
        #password_post=password.post
        
        response = messaging.message(phone_number, message, message_type)
        print("------number is:",phone_number)
        
        print("------------Response: ",response)
        print("-------------post.text: ",post.text)
        print("------------Code: ", verify_code)
        print("------------Email: ", email_post)
        print("------------Password: ", password_post)
        
        
        
        
        
        if post.text == verify_code:
            response_data['author'] = 'WIN'
            print("--------------Success!!")
        else:
            print("--------------No match!!")
        

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
    
