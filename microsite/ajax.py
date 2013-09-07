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
import datetime

from framework.models import Account, WXAccount
from microsite.models import Menu
from microsite.forms import AddEditMenuForm
from microsite.forms import AddCaseClassForm, ChangeCaseClassForm, AddProductClassForm, ChangeProductClassForm
from microsite.models import CaseClass, ProductClass
from microsite.models import ContactPeople
from microsite.forms import AddEditContactPeopleForm

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

