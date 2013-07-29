var toast = function(type, text) {
    $.pnotify({
        text: text,
        type: type,
        delay: 3000,
        history: false,
        stack: false,
        closer: false,
        sticker: false,
        before_open: function(pnotify) {
            pnotify.css({
                "top": ($(window).height() / 2) - (pnotify.height() / 2),
                "left": ($(window).width() / 2) - (pnotify.width() / 2)
            });
        }
    });
};

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