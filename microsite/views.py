# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render_to_response, get_object_or_404, render, redirect

from forms import *
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from models import *
from tables import ContactPeopleTable, MenuTable
from app_manager import AppMgr
from framework.models import *
from datetime import datetime
from microsite.forms import MenuForm

from wx_match import *

logger = logging.getLogger('default')

def get_tabs(request):
    user = auth.get_user(request)
    account = Account.objects.get(user=user)

    wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    pages = Page.objects.filter(wx=wx)
    tabs = []
    logger.debug("wx id %d" % wx.pk)
    for p in pages:
        subp = p.cast()
        form = FormManager.get_form(subp)
        tabs.append( (subp, form) )
    return tabs

def get_apps(request):
    user = auth.get_user(request)
    account = Account.objects.get(user=user)
    wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    apps = App.objects.filter(wx=wx)
    return apps

def get_tabs_names(request):
    user = auth.get_user(request)
    account = Account.objects.get(user=user)
    wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    pages = Page.objects.filter(wx=wx)
    tabs_names = []
    for p in pages:
        tabs_names.append(p.tab_name)
    return tabs_names

@login_required
def settings(request, active_tab_id = None):
    if active_tab_id:
        active_tab_id = int(active_tab_id)
    else:
        active_tab_id = 0
    user = auth.get_user(request)
    account = Account.objects.get(user=user)

    wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    request.session['active_wx_id'] = wx.pk
    tabs = get_tabs(request)
    if active_tab_id > len(tabs):
        active_tab_id = 0
    apps = get_apps(request)
    return render(request, "settings.html", {"tabs":tabs, "active_tab_id":active_tab_id, 'page':tabs[active_tab_id][0], 'f':tabs[active_tab_id][1], 'apps':apps, 'active_side_id':-1})

@login_required
@page_verify('app_id')
def app(request, app_id):
    app_id = int(app_id)
    if not request.user.is_authenticated():
        logger.debug("not login")
        return redirect('/login')
    apps = get_apps(request)
    active_side_id = 1
    for i in range(len(apps)):
        logger.debug("pk %d app_id %d" % (apps[i].pk, app_id))
        if apps[i].pk == app_id:
            active_side_id = i + 1
            app_info = AppMgr.get_app_info(apps[i].cast())
            active_app = apps[i]
            active_app_specific= AppMgr.get_app_enable(apps[i].cast())
    logger.debug("active side id is %d" % active_side_id)

    tabs_names=get_tabs_names(request)
    tab_id=tabs_names.index(active_app_specific.title)
    logger.debug("tab id is %d" % tab_id)
    
    return render(request, 'app.html', {'apps':apps, 'active_side_id':active_side_id, 'app_info':app_info, 'active_app':active_app, 'active_app_specific':active_app_specific, 'tab_id':tab_id})

@login_required
@page_verify('page_id')
def save(request, page_id):
    if page_id:
        page_id = int(page_id)
        tabs = get_tabs(request)
        active_tab_id = -1
        for i in range(len(tabs)):
            if tabs[i][0].pk == page_id:
                active_tab_id = i
                logger.debug("find form active tab id %d" % i)
                break

        if active_tab_id == -1:
            return redirect('/setting')

        apps = get_apps(request)

        logger.debug("save page id %d" % page_id)
        page = get_object_or_404(Page, id = page_id)
        sub_page = page.cast()
        form = FormManager.get_form(sub_page, request)
        if request.method == 'POST':
            if form.is_valid():
                intropage = form.save()
                intropage.save()
                return render(request, "settings.html", {"tabs":tabs, "active_tab_id":active_tab_id, 'page':sub_page, 'f':form, 'apps':apps, 'active_side_id':-1})
            else:
                logger.debug("form is not valid")
                return render(request, "settings.html", {"tabs":tabs, "active_tab_id":active_tab_id, 'page':sub_page, 'f':form, 'apps':apps, 'active_side_id':-1})
        else:
            return redirect("/setting/%d" % active_tab_id)
    else:
        logger.error("no page id")
    return redirect("/setting")

@login_required
@contact_item_verify('item_id')
def add_edit_contact(request, item_id=None):
    if item_id:
        item = get_object_or_404(ContactItem, pk = item_id)
        peoples = ContactPeopleTable(ContactPeople.objects.filter(contact_item=item))
    else:
        peoples = None
        item = None
    if request.method == 'POST':
        form = ContactItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                user = auth.get_user(request)
                account = Account.objects.get(user=user)
                wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
                contact_app = ContactApp.objects.get(wx=wx)
                item.contact = contact_app
            item.save()
            return redirect('/app/%d' % item.contact.id)
    else:
        form = ContactItemForm(instance=item)

    return render(request, 'add_edit_contact.html', {'form':form, 'peoples':peoples, 'contact_id':item_id})

@login_required
@contact_item_verify('item_id')
def contact_delete(request, item_id):
    item = get_object_or_404(ContactItem, pk = item_id)
    id = item.contact.pk
    peoples = ContactPeople.objects.filter(contact_item=item)
    for p in peoples:
        p.delete()
    item.delete()
    return redirect('/app/%d' % id)


@login_required
@contact_people_verify('item_id')
def add_edit_contact_people(request, item_id=None):
    if item_id:
        item = get_object_or_404(ContactPeople, pk = item_id)
    else:
        item = None
    wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
    contact_app = ContactApp.objects.get(wx=wx)
    if request.method == 'POST':
        form = ContactPeopleForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('/app/%d' % item.contact_item.contact.pk)
    else:
        form = ContactPeopleForm(instance=item)

    form.fields['contact_item'].queryset = ContactItem.objects.filter(contact=contact_app)
    return render(request, 'add_edit_contact_people.html', {'form':form})

@login_required
@contact_people_verify('item_id')
def contact_people_delete(request, item_id):
    item = get_object_or_404(ContactPeople, pk = item_id)
    id = item.contact_item.pk
    item.delete()
    return redirect('/contact/%d/edit' % id)

@login_required
@trend_item_verify('item_id')
def add_edit_trend(request, item_id=None):
    if item_id:
        item = get_object_or_404(TrendItem, pk = item_id)
    else:
        peoples = None
        item = None
    if request.method == 'POST':
        form = TrendItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                user = auth.get_user(request)
                account = Account.objects.get(user=user)
                wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
                trends_app = TrendsApp.objects.get(wx=wx)
                item.trend = trends_app
            item.pub_time = datetime.now()
            item.save()
            return redirect('/app/%d' % item.trend.id)
    else:
        form = TrendItemForm(instance=item)

    return render(request, 'add_edit_trend.html', {'form':form})

@login_required
@trend_item_verify('item_id')
def trend_delete(request, item_id):
    item = get_object_or_404(TrendItem, pk = item_id)
    app_id = item.trend.pk
    item.delete()
    return redirect('/app/%d' % app_id)

@login_required
@page_verify('link_id')
def add_edit_link_page(request, link_id=None):
    if link_id:
        item = get_object_or_404(LinkPage, pk = link_id)
    else:
        item = None
    if request.method == 'POST':
        form = LinkPageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                user = auth.get_user(request)
                account = Account.objects.get(user=user)
                wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
                item.enable = True
                item.wx = wx
            item.save()
            return redirect('/setting')
    else:
        form = LinkPageForm(instance=item)

    return render(request, 'add_edit_link.html', {'form':form})

@login_required
@page_verify('content_id')
def add_edit_content_page(request, content_id=None):
    if content_id:
        item = get_object_or_404(ContentPage, pk = content_id)
    else:
        item = None
    if request.method == 'POST':
        form = ContentPageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                user = auth.get_user(request)
                account = Account.objects.get(user=user)
                wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
                item.enable = True
                item.wx = wx
            item.save()
            return redirect('/setting')
    else:
        form = ContentPageForm(instance=item)

    return render(request, 'add_edit_content.html', {'form':form})
    
@login_required
@case_item_verify('item_id')
def add_edit_case(request, item_id=None):
    if item_id:
        item = get_object_or_404(CaseItem, pk = item_id)
    else:
        item = None
    wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
    case_app = CaseApp.objects.get(wx=wx)
    if request.method == 'POST':
        form = CaseItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                item.case_app= case_app
            item.pub_time = datetime.now()
            logger.debug("item picurl %s" % item.case_pic1)
            item.save()
            return redirect('/app/%d' % item.case_app.id)
    else:
        form = CaseItemForm(instance=item)
    form.fields['cls'].queryset = CaseClass.objects.filter(case_app=case_app)

    return render(request, 'add_edit_case.html', {'form':form})

@login_required
@case_class_verify('item_id')
def add_edit_case_class(request, item_id=None):
    if item_id:
        item = get_object_or_404(CaseClass, pk = item_id)
    else:
        item = None
    if request.method == 'POST':
        form = CaseClassForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
                case_app = CaseApp.objects.get(wx=wx)
                item.case_app= case_app
            item.pub_time = datetime.now()
            item.save()
            return redirect('/app/%d' % item.case_app.id)
    else:
        form = CaseClassForm(instance=item)

    return render(request, 'add_edit_case_class.html', {'form':form})

@login_required
@case_item_verify('item_id')
def case_delete(request, item_id):
    item = get_object_or_404(CaseItem, pk = item_id)
    app_id = item.case_app.id
    item.delete()
    return redirect('/app/%d' % app_id)

@login_required
@case_class_verify('item_id')
def case_class_delete(request, item_id):
    item = get_object_or_404(CaseClass, pk = item_id)
    cases = CaseItem.objects.filter(cls=item)
    for c in cases:
        c.delete()
    app_id = item.case_app.pk
    item.delete()
    return redirect('/app/%d' % app_id)

@login_required
@product_item_verify('item_id')
def add_edit_product(request, item_id=None):
    if item_id:
        item = get_object_or_404(ProductItem, pk = item_id)
    else:
        item = None
    wx_account = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
    product_app = ProductApp.objects.get(wx=wx_account)
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                user = auth.get_user(request)
                account = Account.objects.get(user=user)
                item.product_app= product_app
            item.pub_time = datetime.now()
            item.save()
            return redirect('/app/%d' % item.product_app.id)
    else:
        form = ProductItemForm(instance=item)

    form.fields['cls'].queryset = ProductClass.objects.filter(product_app=product_app)

    return render(request, 'add_edit_product.html', {'form':form})

@login_required
@product_class_verify('item_id')
def add_edit_product_class(request, item_id=None):
    if item_id:
        item = get_object_or_404(ProductClass, pk = item_id)
    else:
        item = None
    if request.method == 'POST':
        form = ProductClassForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                wx= get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
                product_app = ProductApp.objects.get(wx=wx)
                item.product_app= product_app
            item.pub_time = datetime.now()
            item.save()
            return redirect('/app/%d' % item.product_app.id)
    else:
        form = ProductClassForm(instance=item)

    return render(request, 'add_edit_product_class.html', {'form':form})

@login_required
@product_class_verify('item_id')
def product_class_delete(request, item_id):
    item = get_object_or_404(ProductClass, pk = item_id)
    products = ProductItem.objects.filter(cls=item)
    for p in products:
        p.delete()
    app_id = item.product_app.pk
    item.delete()
    return redirect('/app/%d' % app_id)

 
@login_required
@product_item_verify('item_id')
def product_delete(request, item_id):
    item = get_object_or_404(ProductItem, pk = item_id)
    app_id = item.product_app.pk
    item.delete()
    return redirect('/app/%d' % app_id)

@login_required
def menu0(request):
    apps = get_apps(request)
    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    else:
        return redirect('/bind')

    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            wx_account.app_id = form.cleaned_data.get('app_id')
            wx_account.app_secret = form.cleaned_data.get('app_secret')
            wx_account.save()
            
            cache.set(wx_account.id, form.cleaned_data.get('access_token'), 7200)
            return redirect('/menu')
    else:
        form = MenuForm()
    return render(request, 'menu0.html', {'apps' : apps, 'form' : form})

@login_required
def menu(request):
    apps = get_apps(request)
    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    else:
        return redirect('/bind')

    if wx_account.app_id is None or wx_account.app_secret is None:
        return redirect('/menu0')
    else:
        menu_info = MenuTable(Menu.objects.filter(wx=wx_account))
        return render(request, 'menu.html', {'apps' : apps, 'menu_info' : menu_info})