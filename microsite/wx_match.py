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

            

