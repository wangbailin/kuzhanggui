#coding:utf-8
import logging
from functools import wraps
from django.contrib import auth

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from framework.models import WXAccount, Account
from models import *

logger = logging.getLogger('default')

def page_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            page = get_object_or_404(Page, pk=kwargs[id_name])
            if page.wx.pk != active_wx_id:
                logger.debug("page verify failed active wx id is %d, page.wx id is %d" % (active_wx_id, page.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

def contact_item_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            item = get_object_or_404(ContactItem, pk=kwargs[id_name])
            if item.contact.wx.pk != active_wx_id:
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, item.contact.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

def contact_people_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            people = get_object_or_404(ContactPeople, pk=kwargs[id_name])
            contact_item = people.contact_item
            if contact_item.contact.wx.pk != active_wx_id:
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, contact_item.contact.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

def trend_item_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            trend_item= get_object_or_404(TrendItem, pk=kwargs[id_name])
            if trend_item.trend.wx.pk != active_wx_id:
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, trend_item.trend.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate
def case_item_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            case_item = get_object_or_404(CaseItem, pk=kwargs[id_name])
            if case_item.case_app.wx.pk != active_wx_id:
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, case_item.case_app.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

def case_class_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            case_class= get_object_or_404(CaseClass, pk=kwargs[id_name])
            if case_class.case_app.wx.pk != active_wx_id:
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, case_class.case_app.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

def product_class_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            product_class= get_object_or_404(ProductClass, pk=kwargs[id_name])
            if product_class.product_app.wx.pk != active_wx_id:
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, product_class.product_app.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

def product_item_verify(id_name):
    def real_decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            active_wx_id = request.session.get('active_wx_id', 0)
            if active_wx_id <= 0:
                logger.debug("active_wx_id is %d" % active_wx_id)
                return redirect('/settings')
            wx = get_object_or_404(WXAccount, pk=active_wx_id)
            if id_name not in kwargs:
                logger.debug("%s not in kwargs %s" % (id_name, str(kwargs)))
                return redirect('/settings')
            if kwargs[id_name] is None:
                return func(request, *args, **kwargs)
            product_item= get_object_or_404(ProductItem, pk=kwargs[id_name])
            if product_item.product_app.wx.pk != active_wx_id:
                logger.debug("verify failed active wx id is %d, item.wx id is %d" % (active_wx_id, product_item.product_app.wx.pk))
                return redirect('/settings')
            else:
                return func(request, *args, **kwargs)
        return wrapper
    return real_decorate

