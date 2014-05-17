# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import json
import random
import datetime
import logging

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.db import transaction
from dajax.core import Dajax
from django.core.cache import cache
from django.db.models import Max
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from rocket import settings
from framework.models import Account, WXAccount
from microsite.forms import JoinItemForm, AddCaseClassForm, ChangeCaseClassForm, AddProductClassForm, ChangeProductClassForm, AddEditMenuForm, AddEditContactPeopleForm
from microsite.models import *
from utils import get_wx_access_token, create_wx_menu

logger = logging.getLogger('default')

@transaction.commit_on_success
def add_menu(wx_account, name, page_ids):
    menu = Menu(wx=wx_account, name=name)
    menu.save()
    modify_menu_items(menu, page_ids)

@transaction.commit_on_success
def edit_menu(id, name, page_ids):
    menu = Menu.objects.get(id=id)
    menu.name = name
    menu.save()
    PageGroup.objects.filter(menu=menu).delete()
    modify_menu_items(menu, page_ids)

def modify_menu_items(menu, page_ids):
    for index in range(len(page_ids)):
        page_id = page_ids[index]
        page = Page.objects.get(pk=page_id)
        pageGroup = PageGroup(page=page, menu=menu, position=index)
        pageGroup.save()

def menu_name_exists(name, exclude=None):
    if exclude is None:
        return Menu.objects.filter(name=name).exists()
    else:
        return Menu.objects.filter(name=name).exclude(pk=exclude).exists()


def ensure_wx_account(user):
    account = Account.objects.get(user=request.user)
    wx_account = None
    if acount.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    return wx_account


@dajaxice_register
def add_edit_trend_category(request, id, name):
    wx_account = ensure_wx_account(request.user)
    if wx_account is None:
        logger.error("add_edit_trend_category: wx account not found")
        return simplejson({'ret_code': 1000, 'ret_msg': u'微信账号未绑定'})

    if name is None or name == '':
        logger.error("add_edit_trend_category: name is invalid")
        return simplejson.dumps({'ret_code': 1000, 'ret_msg': u'名称是必填项'})

    app = TrendsApp.objects.get(wx=wx_account)
    if id is None or id == '':
        if len(TrendCategory.objects.filter(app=app).exclude(pk=id).filter(name=name)) > 0:
            logger.error("add_edit_trend_category: duplicated name")
            return simplejson.dumps({'ret_code': 1000, 'ret_msg': u'分类已存在'})
        category = TrendCategory.objects.get(pk=id)
        category.app = app
        category.name = name
        category.save()
    else:
        if len(TrendCategory.objects.filter(name=name).filter(app=app)) > 0:
            logger.error("add_edit_trend_category: duplicated name")
            return simplejson.dumps({'ret_code': 1000, 'ret_msg': u'分类已存在'})
        TrendCategory(app=app, name=name).save()

    return simplejson.dumps({'ret_code': 0})


@dajaxice_register
def add_edit_menu(request, id, name, pages):
    #raise Exception()
    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    if name is None or name == '':
        ret_msg = '名称是必填项'
        logger.error("add_edit_menu form is invalid, msg %s" % ret_msg)
        return simplejson.dumps({'ret_code': 1000, 'ret_msg': ret_msg})
    elif pages is None or pages == '':
        ret_msg = '显示页面是必填项'
        logger.error("add_edit_menu form is invalid, msg %s" % ret_msg)
        return simplejson.dumps({'ret_code': 1000, 'ret_msg': ret_msg})

    page_ids = [int(p) for p in pages.split(',')]
    logger.debug("pages' id: " + str(page_ids))

    if id is not None and id != '':
        if menu_name_exists(name, exclude=id):
            return simplejson.dumps({'ret_code': 1000, 'ret_msg': '菜单名称已存在'})

        edit_menu(id, name, page_ids)
        return simplejson.dumps({'ret_code': 0})
    else:
        if menu_name_exists(name):
            return simplejson.dumps({'ret_code': 1000, 'ret_msg': '菜单名称已存在'})

        add_menu(wx_account, name, page_ids)
        return simplejson.dumps({'ret_code': 0})

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
            contact_item=form.cleaned_data.get('contact_item')
            max_pos = contact_item.contactpeople_set.all().aggregate(Max('position'))
            position = int(max_pos['position__max'] or 0) + 1
            ContactPeople.objects.create(contact_item=contact_item, name=form.cleaned_data.get('name'), qq=form.cleaned_data.get('qq'), phone=form.cleaned_data.get('phone'), email=form.cleaned_data.get('email'),position=position)
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
def add_edit_join_item(request, form):
    dajax = Dajax()
    form = JoinItemForm(deserialize_form(form))
    if form.is_valid():
        if form.cleaned_data.get('id'):
            joinItem = JoinItem.objects.filter(id=form.cleaned_data.get('id'))[0]
            joinItem.publish = form.cleaned_data.get('publish')
            joinItem.job_title = form.cleaned_data.get('job_title')
            joinItem.number = form.cleaned_data.get('number')
            joinItem.content1 = form.cleaned_data.get('content1')
            joinItem.content2 = form.cleaned_data.get('content2')
            joinItem.content3 = form.cleaned_data.get('content3')
            joinItem.content4 = form.cleaned_data.get('content4')
            joinItem.require1 = form.cleaned_data.get('require1')
            joinItem.require2 = form.cleaned_data.get('require2')
            joinItem.require3 = form.cleaned_data.get('require3')
            joinItem.require4 = form.cleaned_data.get('require4')
            joinItem.save()
        else:
            join_id=form.cleaned_data.get('tab_id')
            joinapp = JoinApp.objects.get(pk=join_id)
            max_pos = joinapp.joinitem_set.all().aggregate(Max('position'))
            position = int(max_pos['position__max'] or 0) + 1
            JoinItem.objects.create(join_id=join_id, publish=form.cleaned_data.get('publish'), job_title=form.cleaned_data.get('job_title'), number=form.cleaned_data.get('number'), content1=form.cleaned_data.get('content1'), content2=form.cleaned_data.get('content2'), content3=form.cleaned_data.get('content3'), content4=form.cleaned_data.get('content4'), require1=form.cleaned_data.get('require1'), require2=form.cleaned_data.get('require2'), require3=form.cleaned_data.get('require3'), require4=form.cleaned_data.get('require4'), position=position)
        dajax.remove_css_class('#add_edit_join_item_form.control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : 'success' }, 'addEditJoinItemCallback')
        dajax.redirect(form.cleaned_data.get('tab_id'))
    else:
        dajax.remove_css_class('#add_edit_join_item_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'addEditJoinItemCallback')

    return dajax.json()

@dajaxice_register
def add_case_class(request, form):
    dajax = Dajax()
    form = AddCaseClassForm(deserialize_form(form))
    if form.is_valid():
        """
        if len(CaseClass.objects.filter(case_app_id=form.cleaned_data.get('tab_id'))) >= 4:
            dajax.remove_css_class('#add_case_class_form .control-group', 'error')
            for error in form.errors:
                dajax.add_css_class('#%s' % error, 'error')
            dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '最多只能添加4个分类！' }, 'addCaseClassCallback')
        else:
        """
        case_app_id = form.cleaned_data.get('tab_id')
        caseapp = CaseApp.objects.get(pk=case_app_id)
        max_pos = caseapp.caseclass_set.all().aggregate(Max('position'))
        position = int(max_pos['position__max'] or 0) + 1
        CaseClass.objects.create(name=form.cleaned_data.get('name'), case_app_id=case_app_id, pub_time=datetime.datetime.now(),position=position)
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
        """
        if len(ProductClass.objects.filter(product_app_id=form.cleaned_data.get('tab_id'))) >= 4:
            dajax.remove_css_class('#add_product_class_form .control-group', 'error')
            for error in form.errors:
                dajax.add_css_class('#%s' % error, 'error')
            dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '最多只能添加4个分类！' }, 'addProductClassCallback')
        else:
        """
        product_app_id=form.cleaned_data.get('tab_id')
        productapp = ProductApp.objects.get(pk=product_app_id)
        max_pos = productapp.productclass_set.all().aggregate(Max('position'))
        position = int(max_pos['position__max'] or 0) + 1
        ProductClass.objects.create(name=form.cleaned_data.get('name'), product_app_id=product_app_id, pub_time=datetime.datetime.now(), position=position)
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

def is_app_menu(menu):
    items = PageGroup.objects.filter(menu=menu)
    if len(items) > 1:
        return False

    subPage = items[0].page.cast()
    caseAppType = ContentType.objects.get_for_model(CaseApp)
    productAppType = ContentType.objects.get_for_model(ProductApp)
    return subPage.real_type == caseAppType or subPage.real_type == productAppType


def generate_menu_json(wx_account):
    view_fmt = u'{"type": "view", "name": "%s", "url": "%s"}'
    buttons = []
    for menu in wx_account.menu_set.all():
        sub_buttons = []
        menuItems = PageGroup.objects.filter(menu=menu)
        if not is_app_menu(menu):
            if len(menuItems) > 1:
                for item in menuItems[0:4]:
                    values = (item.page.tab_name, settings.SITE_URL + get_page_url(item.page))
                    sub_buttons.append(view_fmt % values)
        else:
            page = menuItems[0].page
            if page.real_type == ContentType.objects.get_for_model(ProductApp):
                product_app = page.cast()
                for cls in product_app.productclass_set.all()[0:4]:
                    sub_buttons.append(view_fmt % (cls.name, settings.SITE_URL+cls.get_url()))
                sub_buttons.append(view_fmt % (u'全部课程', settings.SITE_URL + get_page_url(page)))
            """
            elif page.real_type == ContentType.objects.get_for_model(CaseApp):
                case_app = page.cast()
                for cls in case_app.caseclass_set.all()[0:4]:
                    sub_buttons.append(view_fmt % (cls.name, cls.get_url()))
                sub_buttons.append(view_fmt % (u'全部成功案例', settings.SITE_URL + get_page_url(page)))
            """
        if len(sub_buttons) > 0:
            fmt = u'{ "type": "click", "name": "%s", "sub_button": [%s] }'
            buttons.append(fmt % (menu.name, ','.join(sub_buttons)))
        else:
            buttons.append(view_fmt % (menu.name, settings.SITE_URL + get_page_url(menuItems[0].page)))

    menu_data = u'{"button":[%s]}' % ','.join(buttons)
    logger.debug("menu_data:")
    logger.debug(menu_data)

    return menu_data


@dajaxice_register
def generate_menu(request):
    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    if wx_account is None:
        return json.dumps({'ret_code': 1001, 'ret_msg': '微信号未绑定'})

    menu_data = generate_menu_json(wx_account)

    menu_count = wx_account.menu_set.count()
    if menu_count < 2 or menu_count > 3:
        return json.dumps({'ret_code': 1000, 'ret_msg': '菜单项数量应该为2~3个！'})

    wx_access_token = cache.get('wx_access_token_%d' % wx_account.id, None)
    if wx_access_token is None:
        wx_access_token = get_wx_access_token(wx_account.app_id, wx_account.app_secret)

    if wx_access_token is None:
        return json.dumps({'ret_code': 1001, 'ret_msg': '微信系统繁忙，请重试生成菜单'})

    if create_wx_menu(wx_access_token, menu_data):
        return json.dumps({'ret_code': 0, 'ret_msg': ''})
    else:
        return json.dumps({'ret_code': 1002, 'ret_msg': '微信系统繁忙，请重试生成菜单!'})


@dajaxice_register
@transaction.commit_manually
def reorder_pages(request, page_list):
    pages = page_list.split(',')
    account = Account.objects.get(user=request.user)
    wx = WXAccount.objects.get(account=account)
    for page_id in pages:
        page = Page.objects.filter(pk=page_id, wx=wx)
        if len(page) != 1 or not page[0].enable:
            return simplejson.dumps({'ret_code': 1000, 'ret_msg': '数据出错，请稍后重试。'})

    try:
        for i in range(len(pages)):
            page_id = pages[i]
            page = Page.objects.get(pk=page_id)
            subp = page.cast()
            subp.position = i + 1
            subp.save()
        #raise Exception()
    except Exception as e:
        logger.exception("reorder_pages error")
        transaction.rollback()
        raise e
    else:
        transaction.commit()
        return simplejson.dumps({'ret_code': 0, 'ret_msg': '操作成功'})



@dajaxice_register
def homepage_available_options(request):
    dajax = Dajax()

    account = Account.objects.get(user=request.user)
    wx = WXAccount.objects.get(account=account)

    pages = Page.objects.filter(wx=wx, enable=True)

    links = []
    options = []
    output = []
    for page in pages:
        options.append({
            "name": page.tab_name, 
            "url": get_page_url(page)
        })
        #get the links which are already stored in HomePage.
        if page.real_type == ContentType.objects.get_for_model(HomePage):
            homepage = page.cast()
            links = [homepage.link1, homepage.link2, homepage.link3, homepage.link4]
        if page.real_type == ContentType.objects.get_for_model(TrendsApp):
            page = page.cast()
            items = page.trenditem_set.all()
            for item in items:
                options.append({
                    "name": page.tab_name + '--' + item.title, 
                    "url": get_item_url(item)
                })
        elif page.real_type == ContentType.objects.get_for_model(CaseApp):
            page = page.cast()
            items = page.caseitem_set.all()
            for item in items:
                options.append({
                    "name": page.tab_name + '--' + item.title, 
                    "url": get_item_url(item)
                })
        elif page.real_type == ContentType.objects.get_for_model(JoinApp):
            page = page.cast()
            items = page.joinitem_set.all()
            for item in items:
                options.append({
                    "name": page.tab_name + '--' + item.job_title, 
                    "url": get_item_url(item)
                })
        elif page.real_type == ContentType.objects.get_for_model(ProductApp):
            page = page.cast()
            items = page.productitem_set.all()
            for item in items:
                options.append({
                    "name": page.tab_name + '--' + item.title, 
                    "url": get_item_url(item)
                })

    return json.dumps({
        "options": options,
        "links": links
    })
    

@dajaxice_register
def reorder_items(request, items):
    dajax = Dajax()
    try:
        for item in items:
            if item[0] == "JoinItem" :
                JoinItem.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "TrendItem":
                TrendItem.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "CaseClass":
                CaseClass.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "CaseItem":
                CaseItem.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "ProductClass":
                ProductClass.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "ProductItem":
                ProductItem.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "TeamItem":
                TeamItem.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "ContactItem":
                ContactItem.objects.filter(pk=item[1]).update(position=item[2])
            elif item[0] == "ContactPeople":
                ContactPeople.objects.filter(pk=item[1]).update(position=item[2])
            else:
                dajax.add_data({'ret_code ': 1001, 'ret_msg' : '数据出错，请稍后再试'},'reorderItemCallback')
    except Exception as e:
        logger.exception("reorder_pages error")
        dajax.add_data({'ret_code' : 1000, 'ret_msg' : '保存失败'},'reorderItemCallback')
        raise e
    else:
        dajax.add_data({'ret_code' : 0, 'ret_msg' : '保存成功！'},'reorderItemCallback')
    return dajax.json()
