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

var login_page = document.querySelector("#loginPage");
var main_page = document.querySelector('#mainPage');

function login() {
    login_page.classList.add('d-none');

    if(main_page.classList.contains('d-none')){
        main_page.classList.remove('d-none');
    }
}

function logout(){
    main_page.classList.add('d-none');

    if (login_page.classList.contains('d-none')){
        login_page.classList.remove('d-none');

    }
}