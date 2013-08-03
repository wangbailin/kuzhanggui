var changePassword = function() {
    $('#change_password_save').button('loading');
    Dajaxice.framework.change_password(Dajax.process, {'form' : $('#change_password_form').serialize(true)});
};

var changePasswordCallback = function(data) {
    if (data && data.ret_code == 0) {
        $('#change_password').modal('hide');
        toast('success', '密码修改成功！')
    }

    $('#change_password_save').button('reset');
};