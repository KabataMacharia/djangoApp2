$(function() {
    $("#id_code").hide()
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

    // AJAX for posting
    function ajax_user_login() {
        status = "";
        
        console.log("user_login is working!") // sanity check
        $.ajax({
            url : "/login/", // the endpoint
            type : "POST", // http method
            data : { username: $('#username').val(), password: $('#password').val() },    
                        
            // handle a successful response
            success : function(json) {                
                console.log("Json.logged_in is:",json.logged_in); // log the returned json to the console
                
                
                if(typeof json.logged_in =='string'){
                
                $("h3:first").replaceWith("<h3>Now enter the sms code<h3>");                
                $("div.username_pass").hide()
                 $("#id_code").show() 
                 status = "DONE";               
                                    }   
                console.log("Status inside user_login: ",status); // another sanity check
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
            url : "/verify/", // the endpoint
            type : "POST", // http method
            data : { code: $('#id_code').val()},    
                        
            // handle a successful response
            success : function(json) {                
                console.log("Json.code is:",json.code); // log the returned json to the console
             
                console.log("Status inside user_login: ",status); // another sanity check
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
