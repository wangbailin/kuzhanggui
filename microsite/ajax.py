# -*- coding: utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

import urllib  
import urllib2
import json

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
import random
import datetime

from framework.models import Account, WXAccount
from microsite.forms import AddCaseClassForm, ChangeCaseClassForm, AddProductClassForm, ChangeProductClassForm, AddEditMenuForm, AddEditContactPeopleForm
from microsite.models import CaseClass, ProductClass, Menu, CaseApp, ProductApp, ContactPeople
from utils import get_wx_access_token, create_wx_menu

@dajaxice_register
def add_edit_menu(request, form):
    dajax = Dajax()
    form = AddEditMenuForm(deserialize_form(form))

    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    if form.is_valid():
        if form.cleaned_data.has_key('id') and form.cleaned_data.get('id') is not None and form.cleaned_data.get('id') != '':
            menu = Menu.objects.get(id=form.cleaned_data.get('id'))
            menu.name = form.cleaned_data.get('name')
            menu.page = form.cleaned_data.get('page')
        else:
            if Menu.objects.filter(wx=wx_account, name=form.cleaned_data.get('name')).exists():
                dajax.remove_css_class('#add_edit_menu_form .control-group', 'error')
                dajax.add_css_class('#name', 'error')
                dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'addEditMenuCallback')
                return dajax.json()
            else:
                menu = Menu(wx=wx_account, page=form.cleaned_data.get('page'), name=form.cleaned_data.get('name'))
        
        menu.save()
        dajax.remove_css_class('#add_edit_menu_form .control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : 'success' }, 'addEditMenuCallback')
    else:
        dajax.remove_css_class('#add_edit_menu_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'addEditMenuCallback')

    return dajax.json()

@dajaxice_register
def add_edit_contact_people(request, form):
    dajax = Dajax()
    form = AddEditContactPeopleForm(deserialize_form(form))
    if form.is_valid():
        if form.cleaned_data.get('id'):
            contactPeople = ContactPeople.objects.filter(id=form.cleaned_data.get('id'))[0]
            contactPeople.contact_item = form.cleaned_data.get('contact_item')
            contactPeople.name = form.cleaned_data.get('name')
            contactPeople.qq = form.cleaned_data.get('qq')
            contactPeople.email = form.cleaned_data.get('email')
            contactPeople.phone = form.cleaned_data.get('phone')
            contactPeople.save()
        else:
            ContactPeople.objects.create(contact_item=form.cleaned_data.get('contact_item'), name=form.cleaned_data.get('name'), qq=form.cleaned_data.get('qq'), phone=form.cleaned_data.get('phone'), email=form.cleaned_data.get('email'))
        dajax.remove_css_class('#add_edit_contact_people_form.control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : 'success' }, 'addEditContactPeopleCallback')
        dajax.redirect(form.cleaned_data.get('tab_id'))
    else:
        dajax.remove_css_class('#add_edit_contact_people_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'addEditContactPeopleCallback')

    return dajax.json()

@dajaxice_register
def add_case_class(request, form):
    dajax = Dajax()
    form = AddCaseClassForm(deserialize_form(form))
 
    if form.is_valid():
        if len(CaseClass.objects.filter(case_app_id=form.cleaned_data.get('tab_id'))) >= 4:
            dajax.remove_css_class('#add_case_class_form .control-group', 'error')
            for error in form.errors:
                dajax.add_css_class('#%s' % error, 'error')
            dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '最多只能添加4个分类！' }, 'addCaseClassCallback')
        else:
            CaseClass.objects.create(name=form.cleaned_data.get('name'), case_app_id=form.cleaned_data.get('tab_id'), pub_time=datetime.datetime.now())
            dajax.remove_css_class('#add_case_class_form .control-group', 'error')  
            dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'分类已成功添加！' }, 'addCaseClassCallback')
            dajax.redirect(form.cleaned_data.get('tab_id'))

    else:
        dajax.remove_css_class('#add_case_class_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '该分类已添加过！' }, 'addCaseClassCallback')

    return dajax.json()

@dajaxice_register
def add_product_class(request, form):
    dajax = Dajax()
    form = AddProductClassForm(deserialize_form(form))

    if form.is_valid():
        if len(ProductClass.objects.filter(product_app_id=form.cleaned_data.get('tab_id'))) >= 4:
            dajax.remove_css_class('#add_product_class_form .control-group', 'error')
            for error in form.errors:
                dajax.add_css_class('#%s' % error, 'error')
            dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '最多只能添加4个分类！' }, 'addProductClassCallback')
        else:
            ProductClass.objects.create(name=form.cleaned_data.get('name'), product_app_id=form.cleaned_data.get('tab_id'), pub_time=datetime.datetime.now())
            dajax.remove_css_class('#add_product_class_form .control-group', 'error')
            dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'分类已成功添加！' }, 'addProductClassCallback')
            dajax.redirect(form.cleaned_data.get('tab_id'))

    else:
        dajax.remove_css_class('#add_product_class_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '该分类已添加过！' }, 'addProductClassCallback')

    return dajax.json()
 
@dajaxice_register
def change_case_class(request, form):
    dajax = Dajax()
    form = ChangeCaseClassForm(deserialize_form(form))
    if form.is_valid():
        caseClass = CaseClass.objects.filter(id=form.cleaned_data.get('record_id_change'))[0]
        caseClass.name = form.cleaned_data.get('name_change')
        caseClass.pub_time = datetime.datetime.now()
        caseClass.save()
        dajax.remove_css_class('#change_case_class_form .control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'该分类已成功修改！' }, 'changeCaseClassCallback')
        dajax.redirect(form.cleaned_data.get('tab_id_change'))
    else:
        dajax.remove_css_class('#change_case_class_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '该分类已添加过！' }, 'changeCaseClassCallback')

    return dajax.json()

@dajaxice_register
def change_product_class(request, form):
    dajax = Dajax()
    form = ChangeProductClassForm(deserialize_form(form))
    if form.is_valid():
        productClass = ProductClass.objects.filter(id=form.cleaned_data.get('record_id_change'))[0]
        productClass.name = form.cleaned_data.get('name_change')
        productClass.pub_time = datetime.datetime.now()
        productClass.save()
        dajax.remove_css_class('#change_product_class_form .control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'该分类已成功修改！' }, 'changeProductClassCallback')
        dajax.redirect(form.cleaned_data.get('tab_id_change'))
    else:
        dajax.remove_css_class('#change_product_class_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '该分类已添加过！' }, 'changeProductClassCallback')

    return dajax.json()

@dajaxice_register
def generate_menu(request):
    dajax = Dajax()

    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    menu_count = wx_account.menu_set.count()
    if menu_count >= 2 and menu_count <= 3:
        wx_access_token = cache.get('wx_access_token_%d' % wx_account.id, None)
        if wx_access_token is None:
            wx_access_token = get_wx_access_token(wx_account.app_id, wx_account.app_secret)

        if wx_access_token is None:
            dajax.add_data({ 'ret_code' : 1001, 'ret_msg' : '微信系统繁忙，请重试生成菜单' }, 'generateMenuCallback')
        else:
            buttons = []
            for menu in wx_account.menu_set.all():
                sub_buttons = []
                if menu.page.real_type == ContentType.objects.get_for_model(ProductApp):
                    product_app = menu.page.cast()
                    for cls in product_app.productclass_set.all():
                        sub_buttons.append(u'{ "type": "click", "name": "%s", "key": "submenu_%d_%d" }' % (cls.name, menu.id, cls.id))
                elif menu.page.real_type == ContentType.objects.get_for_model(CaseApp):
                    case_app = menu.page.cast()
                    for cls in case_app.caseclass_set.all():
                        sub_buttons.append(u'{ "type": "click", "name": "%s", "key": "submenu_%d_%d" }' % (cls.name, menu.id, cls.id))

                if len(sub_buttons) > 0:
                    buttons.append(u'{ "type": "click", "name": "%s", "sub_button": [%s] }' % (menu.name, ','.join(sub_buttons)))
                else:
                    buttons.append(u'{ "type": "click", "name": "%s", "key": "menu_%d" }' % (menu.name, menu.id))

            menu_data = u'{"button":[%s]}' % ','.join(buttons)
            if create_wx_menu(wx_access_token, menu_data):
                dajax.add_data({ 'ret_code' : 0, 'ret_msg' : '' }, 'generateMenuCallback')
            else:
                dajax.add_data({ 'ret_code' : 1002, 'ret_msg' : '微信系统繁忙，请重试生成菜单!' }, 'generateMenuCallback')
    else:
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '菜单项数量应该为2~3个！' }, 'generateMenuCallback')

    return dajax.json()
