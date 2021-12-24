$("#pass-alert").css("display", "none");
$('#signup-password').keyup(function() {
 if($("#singnup-password").val() === $("#signup-confirm-password").val() && $("#signup-password").val().length > 0){
    $("#registration-btn").removeAttr("disabled");
    $("#pass-alert").css('display', 'none');
 }
 else{
    $("#registration-btn").attr("disabled", "true");
    $("#pass-alert").css('display', 'block');
 }
});
$('#signup-confirm-password').keyup(function() {
 if($("#signup-password").val() === $("#signup-confirm-password").val() && $("#signup-password").val().length > 0){
    $("#registration-btn").removeAttr("disabled");
    $("#pass-alert").css('display', 'none');
 }
 else{
    $("#registration-btn").attr("disabled", "true");
    $("#pass-alert").css('display', 'block');
 }
});




function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function Registration(event){
    event.preventDefault();

    $.ajax({
        url:"/auth/",
        type:"POST",
        data:{
            first_name: $("#signup-first-name").val(),
            last_name: $("#signup-last-name").val(),
            email: $("#signup-email").val(),
            password: $("#signup-password").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(result) {
            if (result.success === 'yes'){
                document.getElementById('signin-tab').click();
                $("#registration-form")[0].reset();
            }
            alert(result.msg);
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        error: function(e){
            console.error(JSON.stringify(e));
        },
    });
  }

function Login(event){
    event.preventDefault();

    $.ajax({
        url:"/auth/",
        type:"POST",
        data:{
            email: $("#signin-email").val(),
            password: $("#signin-password").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(result) {
            alert(result.item);
        },
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        error: function(e){
            console.error(JSON.stringify(e));
        },
    });
  }