$(function() {


    
    // Submit post on submit
    $('#login_form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        ajax_user_login();
        
    });    
        

    // AJAX for posting
    function ajax_user_login() {
        console.log("user_login is working!") // sanity check
        $.ajax({
            url : "/login/", // the endpoint
            type : "POST", // http method
            data : { username: $('#username').val(), password: $('#password').val(), phone_number: $('#id_phone_number').val(), code:$('#id_code').val() },
                        
            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log("Json.user is:"); // log the returned json to the console
                console.log(json.logged_in);
                $("h3:first").replaceWith("<h3>Now enter the sms code<h3>");
                $("div.hiders").replaceWith(" ");
                
                
                //$("#talk").prepend("<li><strong>"+json.text+"</strong> - <em> "+json.author+"</em> - <span> "+json.created+
                  //  "</span> - <a id='delete-post-"+json.postpk+"'>delete me</a></li>");  
                  if (json.author == 'WIN')
                  {$("h3:first").replaceWith("<h3>SUCCESS!<h3>");
                    $("div.fieldWrapper").replaceWith("<b>Successfully logged in</b>");
                    $("input.button").replaceWith(" ");
                      }
                      
                if (json.author == 'INVALID')
                  {$("h3:first").replaceWith("<h3>Wrong Username/Password <h3>");
                    $("div.fieldWrapper").replaceWith("<b>You Entered a wrong Username/Password combo</b>");
                    $("input.button").replaceWith(" ");
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
