var login_callback = function(data) {
    if (data.ret_code != 0) {
        toast('error', data.ret_msg);
        $('#login').button('reset');
    } else {
        window.location.href = '/';
    }
};

var login = function() {
    var username = $('#username').val()
    var password = $('#password').val()
    Dajaxice.framework.signin(Dajax.process, { 'username' : username, 'password' : password });

    $('#login').button('loading');
};