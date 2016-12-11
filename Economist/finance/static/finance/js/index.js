/**
 * Created by Rail on 11.12.2016.
 */
$(document).ready(function () {
    var regForm = $('#registration-form');
    var authForm = $('#authorization-form')
    var regBtn = $('#reg-btn');

    //Инициализация элементов Materialize CSS
    $('.parallax').parallax();
    Materialize.updateTextFields();

    //Скрываю формы авторизации и регистрации
    $(regForm).hide();
    $(authForm).hide();

    function showRegistrationForm() {
        $(regForm).fadeIn();
        $(regBtn).addClass('disabled');
    }

    function hideRegistrationForm() {
        $(regForm).fadeOut();
        $(regBtn).removeClass('disabled');
    }

    function showAuthForm() {
        $(authForm).fadeIn();
        $(regBtn).addClass('disabled');
    }

    function hideAuthForm() {
        $(authForm).fadeOut();
        $(regBtn).removeClass('disabled');
    }

    $(regBtn).on('click', function (e) {
        e.preventDefault();
        showRegistrationForm();
    });

    $('#reg_link').on('click', function (e) {
        e.preventDefault();
        showRegistrationForm();
    });

    $('#login_link').on('click', function (e) {
        e.preventDefault();
        showAuthForm();
    });
    //Обработка клика не по нашим формам, что бы закрыть их после этого!
    $(document).mousedown(function (e) {
        var container = $(".card");
        if (!container.is(e.target) // если клик был не по нашему блоку
            && container.has(e.target).length === 0) { // и не по его дочерним элементам
            hideRegistrationForm();
            hideAuthForm();
        }
    });

    //Register user AJAX request
    function register(){
        var url = '/auth/reg';
        var login = $('#login').val();
        if (login.length == 0){
            Materialize.toast('Введите имя пользователя', 4000);
            return;
        }

        var password = $('#password').val();
        if (password.length == 0){
            Materialize.toast('Введите пароль', 4000);
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data:{
                login: login,
                password: password,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function () {
                location.reload();
            }
        })
    }

    function auth(){
        var url = '/auth/auth';
        var login = $('#login_auth').val();
        if (login.length == 0){
            Materialize.toast('Введите имя пользователя', 4000);
            return;
        }

        var password = $('#password_auth').val();
        if (password.length == 0){
            Materialize.toast('Введите пароль', 4000);
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data:{
                login: login,
                password: password,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function () {
                location.reload();
            }
        })
    }

    $('#register').on('click', function (e) {
        e.preventDefault();
        register();
    });

    $('#login_btn').on('click', function (e) {
        e.preventDefault();
        auth();
    });
});