#coding:utf-8
import logging
from functools import wraps
from django.contrib import auth

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from framework.models import WXAccount, Account
from models import *

logger = logging.getLogger('default')

def wx_match(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        active_wx_id = request.session.get('active_wx_id', 0)
        if active_wx_id <= 0:
            logger.debug("active_wx_id is %d" % active_wx_id)
            return redirect('/settings')
        wx = get_object_or_404(WXAccount, pk=active_wx_id)
        account = Account.objects.get(user=request.user)
        if wx.account.pk == account.pk:
            return func(request, *args, **kwargs)
        else:
            logger.debug("wx account pk %d user pk %d" % (wx.account.pk, account.pk))
            return redirect('/settings')
    return wrapper

def app_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/setting')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/setting')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            app = get_object_or_404(App, pk=kwargs[id_name])
            if app.wx.pk != active_wx_id:
                logger.debug("app verify failed active wx id is %d, app.wx id is %d" % (active_wx_id, app.wx.pk))
                return redirect('/setting')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate


    

            

