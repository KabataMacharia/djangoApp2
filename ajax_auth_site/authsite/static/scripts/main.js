$(function() {
    console.log("current URL:",window.location.href);
    
    var code_box = document.getElementById('id_sms_code');
    $('label[for="id_sms_code"]').hide();
    code_box.style.display = 'none';
    var status = "";
    
    // Submit login_form on submit
    $('#login_form').on('submit', function(event){
        event.preventDefault();
        console.log("Status init: ",status);        
        console.log("Submit button activated!");  // sanity check
        if (status == ""){
            ajax_user_login();
        }
        else
        {
            
            code_verify();
            }     
        
    });    
    // register form    
    $('#user_form').on('submit', function(event){
        event.preventDefault();
        console.log("At Register Form!: ",status);        
        console.log("Submit button activated!");  // sanity check 
        register_funct();       
    });    

function register_funct(){
    
    console.log("Inside register_funct");
    $.ajax({
        url: "/register/",
        type : "POST",
        data : {phone_number:$('#id_phone_number').val(), username:$('#id_username').val(), email:$('#id_email').val(), password1:$('#id_password1').val(), password2:$('#id_password2').val() },
           
        success : function(json)
        {
           //anything else I might think of 
           console.log("phone_number",json.phone_number);
           console.log("username",json.username);
           console.log("email",json.email);           
            console.log("uform_errors",json.uform_errors);           
            
            
            //do we have an error? username exists or such stuff
            //console.log("Errors",json.specific_error);
            
            if (json.error_present == 'YES')
            {
                                
                //alert(json.specific_error);
                
                //Display Json errors on relevant field labels                
                var error_array = json.specific_error.split("!");
                error_no = error_array.length;                
                
                //loop through as many errors as are present
                for (i=0; i<error_no; i++)
                {
                    current = (error_array[i]);
                    console.log(current);
                    if (current.includes('email') == true)
                    { 
                        warning = current.replace('email :', '');
                        warning.bold();
                        $('label[for="id_email"]').text ('Email:'+ warning); 
                        $('label[for="id_email"]').css("color", "red"); 
                        }
                        
                    if (current.includes('username') == true)
                    { 
                        warning = current.replace('username :', '');
                        warning.bold();
                        $('label[for="id_username"]').text ('Username:'+ warning); 
                        $('label[for="id_username"]').css("color", "red");                      
                        
                        }
                    if (current.includes('password2') == true)
                    { 
                        warning = current.replace('password2 :', '');
                        warning.bold();
                        $('label[for="id_password2"]').text ('Password2:'+ warning); 
                        $('label[for="id_password2"]').css("color", "red");                      
                        
                        }
                    if (current.includes('phone_number') == true)
                    { 
                        warning = current.replace('phone_number :', '');                        
                        $('label[for="id_phone_number"]').text ('Phone number:'+ warning); 
                        $('label[for="id_phone_number"]').css("color", "red");                      
                        
                        }
                                            
                    }
                
                                
                }
                else
                { 
                    //no error
                    console.log("phone_number",json.phone_number);
                    console.log("username",json.username);
                    console.log("email",json.email); 
                    window.location.replace('/login/');
                    }
            
            }, 
        error : function(xhr,errmsg,err)
        {
            console.log("We have an error!");
            console.log(xhr.status + ": " + xhr.responseText);
            
            }
        });
    
    };

    // AJAX for posting
    function ajax_user_login() {
        status = "";
        
        console.log("user_login is working!") // sanity check
        $.ajax({
            url : "/login/", // the endpoint
            type : "POST", // http method
            data : { username: $('#id_username').val(), password: $('#id_password').val(), code: $('#id_sms_code').val(), csrfmiddlewaretoken: csrftoken, funct:'login'},    
                        
            // handle a successful response
            success : function(json) {                
                console.log("Json.logging_in is:",json.logging_in); // log the returned json to the console
                
                
                if(typeof json.logging_in =='string'){
                
                $("h3:first").replaceWith("<h3>Now enter the sms code<h3>");
                
                //$("div.username_pass").hide()
                //$("#login_link").hide()
                $("#incorrect_userpass").hide();
                 code_box.style.display = ''; 
                 $('label[for="id_sms_code"]').show();
                 status = "DONE";               
                                    }
                    else{
                        //Look into using boostrap here
                        
                        
                        $($("<p id='incorrect_userpass'>The username or password you entered is incorrect</p>").css("color", "red")).insertBefore("#submit_button");
                        
                        //alert("Invalid login credentials.");
                        
                        }
                console.log("Status inside user_login: ",status); 
                
              
                
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };
    
function code_verify ()
{
    console.log("Inside code_verify");
    
            $.ajax({
            url : "/login/", // the endpoint
            type : "GET", // http method
            data : { code: $('#id_sms_code').val(), csrfmiddlewaretoken: csrftoken, funct:'verify'},    
                        
            // handle a successful response
            success : function(json) {
                console.log("Status inside user_login: ",status); // another sanity check                
                console.log("Json.verified is:",json.verified_user); // log the returned json to the console
                
                
                if (json.verified_user == "True")
                {
                    console.log("Hurray! Now do something useful");                    
                    $("h3:first").replaceWith("<h3>Congratulations, successfully verified<h3>");
                    $("form").replaceWith('<form action="/login/"><input type="Submit" value="Go Back" class="tiny button" /></form>');
                    $("#login_link").show()
                    
                    }
                    else
                    {
                        alert("Not the SMS code we sent. Check again");
                        }
                
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
};
     
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
