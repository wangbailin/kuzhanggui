# -*- coding: utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from django.core.cache import cache
from django.contrib.auth import authenticate, login
import random

from utils import send_sms
from models import Account, WXAccount
from forms import ChangePasswordForm, EditAccountForm, ChangePhoneForm
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
def get_url_token(request, name, fans):
    dajax = Dajax()

    account = Account.objects.get(user=request.user)
    wx_account, created = WXAccount.objects.get_or_create(account=account, name=name)

    follower_count = 0
    try:
        follower_count = int(fans)
    except ValueError:
        follower_count = 0

    # generate url and token
    if created:
        wx_account.url = 'http://r.limijiaoyin.com/wx/%d' % wx_account.id
        wx_account.token = str(random.randint(1000,10000))

    wx_account.follower_count = follower_count
    wx_account.save()
    
    cache.set('wx_%d_token' % wx_account.id, wx_account.token, 15 * 60 * 1000)
    dajax.add_data({ 'url' : wx_account.url, 'token' : wx_account.token }, 'getUrlTokenCallback')
    return dajax.json()

@dajaxice_register
def clear_bind_info(request, name):
    dajax = Dajax()

    account = Account.objects.get(user=request.user)
    WXAccount.objects.filter(account=account, name=name).delete()

    if not WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND):
        account.has_wx_bound = False
        account.save()

    return dajax.json()

@dajaxice_register
def is_bind_successed(request, name):
    dajax = Dajax()

    account = Account.objects.get(user=request.user)

    if WXAccount.objects.filter(account=account, name=name, state=WXAccount.STATE_BOUND).exists():
        dajax.add_data({'ret_code' : 0 , 'ret_msg' : 'success'}, 'isBindSuccessedCallback')
    else:
        dajax.add_data({'ret_code' : 1000, 'ret_msg' : 'failed'}, 'isBindSuccessedCallback')

    return dajax.json()

@dajaxice_register
def change_password(request, form):
    dajax = Dajax()
    form = ChangePasswordForm(deserialize_form(form))

    if form.is_valid():
        form.save()
        dajax.remove_css_class('#change_password_form .control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : 'success' }, 'changePasswordCallback')
    else:
        dajax.remove_css_class('#change_password_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'changePasswordCallback')

    return dajax.json()

@dajaxice_register
def edit_account(request, form):
    dajax = Dajax()
    form = EditAccountForm(deserialize_form(form))

    account = Account.objects.get(user=request.user)

    if form.is_valid():
        account.qq = form.cleaned_data.get('qq')
        account.save()
        account.user.email = form.cleaned_data.get('email')
        account.user.save()
        dajax.remove_css_class('#edit_account_form .control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : 'success' }, 'editAccountCallback')
    else:
        dajax.remove_css_class('#edit_account_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'editAccountCallback')

    return dajax.json()

@dajaxice_register
def change_phone(request, form):
    dajax = Dajax()
    form = ChangePhoneForm(deserialize_form(form))

    account = Account.objects.get(user=request.user)

    if form.is_valid():
        account.phone = form.cleaned_data.get('phone')
        account.save()
        dajax.remove_css_class('#change_phone_form .control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : 'success' }, 'changePhoneCallback')
    else:
        dajax.remove_css_class('#change_phone_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'changePhoneCallback')

    return dajax.json()

