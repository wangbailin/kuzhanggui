#coding:utf-8
import logging
from functools import wraps
from django.contrib import auth

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from framework.models import WXAccount, Account
from models import *

logger = logging.getLogger('wall')


def wall_item_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/weixinwall')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return func(request, *args, **kwargs)
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            items = WallItem.objects.filter(pk=kwargs[id_name])
            if len(items) == 0:
                return render(request, 'wall_show_delete.html') 
            else:
                item = items[0]
                if item.wx.pk != active_wx_id:
                    logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, item.wx.pk))
                    return redirect('/weixinwall')
                else:
                    return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

def wall_item_check(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/weixinwall')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return func(request, *args, **kwargs)
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            item = get_object_or_404(WallItem, pk=kwargs[id_name])
            if item.wx.pk != active_wx_id or item.flag_check == '否':
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, item.wx.pk))
                return redirect('/weixinwall')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate
