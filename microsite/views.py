# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render_to_response, get_object_or_404, render, redirect

from forms import *
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from models import *
from tables import TableManager, ContactPeopleTable
from framework.models import *
from datetime import datetime

logger = logging.getLogger('default')

def get_tabs(request):
    user = auth.get_user(request)
    account = Account.objects.get(user=user)
    wx = WXAccount.objects.get(account=account)
    pages = Page.objects.filter(wx=wx)
    tabs = []
    for p in pages:
        subp = p.cast()
        form = FormManager.get_form(subp)
        tabs.append( (subp, form) )
    return tabs

def get_apps(request):
    user = auth.get_user(request)
    account = Account.objects.get(user=user)
    wx = WXAccount.objects.get(account=account)
    apps = App.objects.filter(wx=wx)
    return apps

@login_required
def setting(request, active_tab_id = None):
    if active_tab_id:
        active_tab_id = int(active_tab_id)
    else:
        active_tab_id = 1
    tabs = get_tabs(request)
    apps = get_apps(request)
    return render(request, "setting.html", {"tabs":tabs, "active_tab_id":active_tab_id, 'apps':apps, 'active_side_id':-1})

@login_required
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
            app_info = TableManager.get_table(apps[i].cast())
            active_app = apps[i]
    logger.debug("active side id is %d" % active_side_id)
    
    return render(request, 'app.html', {'apps':apps, 'active_side_id':active_side_id, 'app_info':app_info, 'active_app':active_app})

@login_required
def save(request, page_id):
    if page_id:
        page_id = int(page_id)
        logger.debug("save page id %d" % page_id)
        page = get_object_or_404(Page, id = page_id)
        sub_page = page.cast()
        form = FormManager.get_form(sub_page, request)
        if form.is_valid():
            intropage = form.save()
            intropage.save()
        else:
            logger.debug("form is not valid")
            tabs = get_tabs(request)
            active_tab_id = 1
            for i in range(len(tabs)):
                if tabs[i][0].pk == page_id:
                    tabs[i] = (sub_page, form)
                    active_tab_id = i + 1
                    logger.debug("find form active tab id %d" % (i + 1))
            return render(request, "setting.html", {"tabs":tabs, "active_tab_id":active_tab_id})
    else:
        logger.error("no page id")
    return redirect("/setting")

@login_required
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
                wx = WXAccount.objects.get(account=account)
                contact_app = ContactApp.objects.get(wx=wx)
                item.contact = contact_app
            item.save()
            return redirect('/app/%d' % item.contact.id)
    else:
        form = ContactItemForm(instance=item)

    return render(request, 'add_edit_contact.html', {'form':form, 'peoples':peoples, 'contact_id':item_id})

@login_required
def add_edit_contact_people(request, contact_id, item_id=None):
    if item_id:
        item = get_object_or_404(ContactPeople, pk = item_id)
    else:
        item = None
    if contact_id:
        contact = get_object_or_404(ContactItem, pk = contact_id)
    else:
        return redirect('/')
    if request.method == 'POST':
        form = ContactPeopleForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                item.contact_item = contact
            item.save()
            return redirect('/contact/%d/edit' % int(contact_id))
    else:
        form = ContactPeopleForm(instance=item)

    return render(request, 'add_edit_contact_people.html', {'form':form})

@login_required
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
                wx = WXAccount.objects.get(account=account)
                trends_app = TrendsApp.objects.get(wx=wx)
                item.trend = trends_app
            item.pub_time = datetime.now()
            item.save()
            return redirect('/app/%d' % item.trend.id)
    else:
        form = TrendItemForm(instance=item)

    return render(request, 'add_edit_trend.html', {'form':form})

@login_required
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
                wx = WXAccount.objects.get(account=account)
                item.enable = True
                item.wx = wx
            item.save()
            return redirect('/setting')
    else:
        form = LinkPageForm(instance=item)

    return render(request, 'add_edit_link.html', {'form':form})

@login_required
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
                wx = WXAccount.objects.get(account=account)
                item.enable = True
                item.wx = wx
            item.save()
            return redirect('/setting')
    else:
        form = ContentPageForm(instance=item)

    return render(request, 'add_edit_content.html', {'form':form})
