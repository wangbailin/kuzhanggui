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

var editAccount = function() {
    $('#edit_account_save').button('loading');
    Dajaxice.framework.edit_account(Dajax.process, {'form' : $('#edit_account_form').serialize(true)});
};

var editAccountCallback = function(data) {
    if (data && data.ret_code == 0) {
        $('#edit_account').modal('hide');

        $('#info_email').text($('#email input').val());
        $('#info_qq').text($('#qq input').val());

        toast('success', '账户信息修改成功！')
    }

    $('#edit_account_save').button('reset');
};