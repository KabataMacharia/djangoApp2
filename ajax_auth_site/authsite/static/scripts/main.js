$(function() {


    
    // Submit login_form on submit
    $('#login_form').on('submit', function(event){
        event.preventDefault();
        console.log("Login form submitted!")  // sanity check
        ajax_user_login();
        
    });    
    
// Submit code_form on submit
    $('#code_form').on('submit', function(event){
        event.preventDefault();
        console.log("Code Check form submitted!")  // sanity check
        code_check();
        
    });   
        
    //Create new form for code
var f = document.createElement("form");
//f.innerHTML = '{% csrf_token %}';
f.setAttribute('method',"post");
f.setAttribute('id',"code_form");
f.setAttribute('action',"/login/");
f.setAttribute('class','form_class');


//create input element
var i = document.createElement("input");
i.type = "text";
i.name = "code";
i.id = "id_code";

//csrf
var token = document.createElement("div");
token.setAttribute('class','token_class');



//create a button
var s = document.createElement("input");
s.type = "submit";
s.value = "Submit";
s.class = "tiny button";

// add all elements to the form
f.appendChild(token);
f.appendChild(i);
f.appendChild(s);


    // AJAX for posting
    function ajax_user_login() {
        console.log("user_login is working!") // sanity check
        $.ajax({
            url : "/login/", // the endpoint
            type : "POST", // http method
            data : { username: $('#username').val(), password: $('#password').val(), phone_number: $('#id_phone_number').val(), code:$('#id_code').val() },
    
                        
            // handle a successful response
            success : function(json) {                
                console.log("Json.logged_in is:",json.logged_in); // log the returned json to the console
                console.log("Json.code is:",json.code);
                
                if(typeof json.logged_in =='string'){
                
                $("h3:first").replaceWith("<h3>Now enter the sms code<h3>");
                $("form").replaceWith(" ");
                // add the new form inside the body                
                document.getElementById('form_holder').appendChild(f);
                
                                        
                                    }       
                
                  
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

 // AJAX for posting check_code form
    function code_check() {
        console.log("We are inside code_check!") // sanity check
        
        $.ajax({
            url : "/login/", // the endpoint
            type : "POST", // http method
            data : {code:$('#id_code').val() },      
            csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),       
                        
            // handle a successful response
            success : function(json) {                
                console.log("Json.code is:",json.code);
                
                if(typeof json.logged_in =='string'){
                
                $("h3:first").replaceWith("<h3>Now enter the sms code<h3>");
                $("form").replaceWith(" ");
                // add the new form inside the body
                $( "token_class" ).text( '{% csrf_token %}' );
                document.getElementById('form_holder').appendChild(f);                        
                                    }       
                
                  
                console.log("success"); // another sanity check
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
