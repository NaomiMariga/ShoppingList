$('#signupForm').on('shown.bs.collapse', function () {
  // do something…
    $('#loginForm').collapse('hide');
    $('#pass_reset').collapse('hide');
});

$('#loginForm').on('shown.bs.collapse', function () {
    // execute
    $('#signupForm').collapse('hide');
    $('#pass_reset').collapse('hide');
});

$('#pass_reset').on('shown.bs.collapse', function () {
    $('#signupForm').collapse('hide');
    $('#loginForm').collapse('hide');

});

let login_page = document.querySelector("#loginPage");
let main_page = document.querySelector('#mainPage');

function login() {
    let email = document.querySelector("#login_email").value;
    let password = document.querySelector("#login_password").value;
    $.ajax({
        url: "login",
        type: "POST",
        data: {
            email : email,
            password: password
        },
        dataType: "json",
        success: function (response) {
            let element = document.querySelector("#login_alerts");
            if(response.success){
                window.sessionStorage.setItem("token", response.message.token);
                window.sessionStorage.setItem("user_id", response.message.user_id);
                window.sessionStorage.setItem("username", response.message.username);

                login_page.classList.add('d-none');
                if(main_page.classList.contains('d-none')){
                    main_page.classList.remove('d-none');
                }
            }else{
                 Alert(response.message, element, true);
            }
        }
    })
}
function resetPassword() {
    let email = document.querySelector('#reset_email').value;
    $.ajax({
        url: "reset_password",
        type: "POST",
        data: {
            email: email
        },
        dataType: "json",
        success: function (response) {
          let element = document.querySelector("#reset_password_alerts");
          if(response.success){
              Alert(response.message,element,false)
          }else{
              Alert(response.message,element,true)
          }
        }
    })

}
function logout(){
    main_page.classList.add('d-none');

    if (login_page.classList.contains('d-none')){
        login_page.classList.remove('d-none');

    }
}

let signup = function () {
    let email = document.querySelector("#registration_email").value;
    let username = document.querySelector("#username").value;
    let password = document.querySelector("#registration_password").value;
    $.ajax({
        url: "register",
        type: "POST",
        data: {
            email: email,
            username: username,
            password: password
        },
        dataType:"json",
        success: function (response) {
            let element = document.querySelector("#signup_alerts");
            if(response.success){
                Alert(response.message, element, false);
            }else{
                Alert(response.message, element, true);
            }
        },
        error: function (error) {
          Alert("An error occurred", element, false);
          console.log(error);
        }

    });
};


function Alert(message, element, error)
{
    let close = document.createElement("button");
    close.setAttribute("type","button");
    close.classList.add("close");
    close.setAttribute("data-dismiss","alert");
    close.setAttribute("aria-label","Close");
    let span = document.createElement("span");
    span.setAttribute("aria-hidden","true");
    span.className = "material material-close-circle-o";
    close.appendChild(span);

    let div = document.createElement("div");
    let text = new Text(message);
    div.appendChild(close);
    div.appendChild(text);
    if(error){
        div.className = "alert alert-danger alert-dismissible fade show";
    }else{
        div.className = "alert alert-success alert-dismissible fade show";
    }
    div.setAttribute("role","alert");

    while (element.hasChildNodes()) {
        element.removeChild(element.lastChild);
    }
    element.appendChild(div);
}

