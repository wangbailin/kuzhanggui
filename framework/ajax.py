# -*- coding: utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.core.cache import cache
from django.contrib.auth import authenticate, login
import random

from utils import send_sms
from models import Account, WXAccount

AUTH_CODE_TIMEOUT = 15 * 60 * 1000

@dajaxice_register
def get_auth_code(request, phone):
    dajax = Dajax()
    if Account.objects.filter(phone=phone).exists():
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : u'该手机号码已绑定到其他账号，请使用一个新的手机号码！'}, 'get_auth_code_callback')
    else:
        auth_code = str(random.randint(100000, 1000000))
        send_sms(phone, u"验证码是%s，15分钟内有效" % auth_code)
        cache.set('auth_code_%s' % phone, auth_code, AUTH_CODE_TIMEOUT)
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'已将验证码发送到您的手机，请注意查收。'}, 'get_auth_code_callback')
    return dajax.json()

@dajaxice_register
def signin(request, username, password):
    dajax = Dajax()
    
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'登录成功'}, 'login_callback')
        else:
            dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : u'帐号被锁定，请联系客服！'}, 'login_callback')
    else:
        dajax.add_data({ 'ret_code' : 1001, 'ret_msg' : u'用户名密码不正确，请重新输入！'}, 'login_callback')

    return dajax.json()

@dajaxice_register
def get_url_token(request, name):
    dajax = Dajax()

    account = Account.objects.get(user=request.user)
    wx_account, created = WXAccount.objects.get_or_create(account=account, name=name)

    # generate url and token
    if created:
        wx_account.url = 'http://r.limijiaoyin.com/wx/%d' % wx_account.id
        wx_account.token = str(random.randint(1000,10000))
        wx_account.save()
    
    cache.set('wx_%d_token' % wx_account.id, wx_account.token, 15 * 60 * 1000)
    dajax.add_data({ 'url' : wx_account.url, 'token' : wx_account.token }, 'getUrlTokenCallback')
    return dajax.json()

@dajaxice_register
def clear_bind_info(request, name):
    dajax = Dajax()

    account = Account.objects.get(user=request.user)
    WXAccount.objects.filter(account=account, name=name).delete()

    return dajax.json()