var get_auth_code_callback = function(data) {
    var type = 'success';
    if (data.ret_code != 0) {
        type = 'error';
    }

    toast(type, data.ret_msg);
};

var get_auth_code = function(phone) {
    Dajaxice.framework.get_auth_code(Dajax.process, { 'phone' : phone });

    $('#get_auth_code').button('loading');
    var leftTime = 120;
    var timer = $.timer(1000, function() {
        leftTime = leftTime - 1;
        console.log(leftTime);
        $('#get_auth_code').text('重新获取验证码(' + leftTime + ')');
        if (leftTime <= 0) {
            timer.stop();
            $('#get_auth_code').button('reset');
        }
    });
};