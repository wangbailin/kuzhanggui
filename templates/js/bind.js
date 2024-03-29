var validateUsername = function (el) {
    var username = el.val();
    var retVal = {};

    if (!username || username.length < 6) {
        retVal.status = false;
        retVal.msg = "请输入一个正确的微信公众号用户名";
    } else {
        retVal.status = true;
    }

    return retVal;
}

var validatePassword = function(el) {
    var password = el.val();
    var retVal = {};

    if (!password || password.length < 6) {
        retVal.status = false;
        retVal.msg = "请输入一个正确的微信公众号密码";
    } else {
        retVal.status = true;
    }

    return retVal;
}

var validateName = function (el) {
    var name = el.val();
    var retVal = {};

    if (!name || name.length < 2) {
        retVal.status = false;
        retVal.msg = "请输入一个正确的微信公众号名称";
    } else {
        retVal.status = true;
    }

    return retVal;
}

var wxAccountName = '';

var getUrlToken = function() {
    if (!$(this).hasClass('disabled')) {
        $('#get_url_token').button('loading');

        wxAccountName = $('#wxaccount_name').val();
        wxAccountFans = $('#wxaccount_fans').val();
        Dajaxice.framework.get_url_token(Dajax.process, { 'name' : wxAccountName, 'fans' : wxAccountFans });
    }
}

var getUrlTokenCallback = function(data) {
    if (data) {
        $('#wxaccount_url').text(data.url);
        $('#wxaccount_token').text(data.token);
        $('#wxaccount_restart').removeClass('disabled');
        $('#wxaccount_bound').removeClass('disabled');
    }

    $('#get_url_token').button('reset');
}

var clearBindInfo = function() {
    if (!$(this).hasClass('disabled')) {
        if (wxAccountName) {
            Dajaxice.framework.clear_bind_info(Dajax.process, { 'name' : wxAccountName });
        }

        wxAccountName = '';
        $('#wxaccount_name').val('');
        $('#wxaccount_url').text('');
        $('#wxaccount_token').text('');
        $('#wxaccount_restart').addClass('disabled');
        $('#wxaccount_bound').addClass('disabled');

        $('html,body').animate({scrollTop:0},'slow');
    }
}

var isBindSuccessed = function() {
    if (!$(this).hasClass('disabled')) {
        if (wxAccountName) {
            Dajaxice.framework.is_bind_successed(Dajax.process, { 'name' : wxAccountName });
        }
    }
}

var isBindSuccessedCallback = function(data) {
    if (data && data.ret_code == 0) {
        window.location.href = '/';
    } else {
        toast('error', '绑定失败，请确认接口信息填写正确。');
    }
}