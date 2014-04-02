# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.db import transaction
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Max

from forms import *
from models import *
from tables import ContactPeopleTable, MenuTable
from app_manager import AppMgr
from framework.models import *
from datetime import datetime
from microsite.forms import MenuForm
import django_tables2 as tables

from wx_match import *

logger = logging.getLogger('default')

def get_tabs(request):
    if 'active_wx_id' in request.session:
        wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
    else:
        user = auth.get_user(request)
        account = Account.objects.get(user=user)

        wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
        request.session['active_wx_id'] = wx.pk
    pages = Page.objects.filter(wx=wx).order_by('position')
    tabs = []
    logger.debug("wx id %d" % wx.pk)
    for p in pages:
        subp = p.cast()
        form = FormManager.get_form(subp)
        tabs.append( (subp, form) )
    return tabs

def get_apps(request):
    if 'active_wx_id' in request.session:
        wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
    else:
        user = auth.get_user(request)
        account = Account.objects.get(user=user)

        wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
        request.session['active_wx_id'] = wx.pk

    apps = App.objects.filter(wx=wx)
    return apps

def get_tabs_names(request):
    if 'active_wx_id' in request.session:
        wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
    else:
        user = auth.get_user(request)
        account = Account.objects.get(user=user)

        wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    pages = Page.objects.filter(wx=wx)
    tabs_names = []
    for p in pages:
        tabs_names.append(p.tab_name)
    return tabs_names

@cal_time
@login_required
@bind_wx_check
def settings(request, active_tab_id = None):
    user = auth.get_user(request)
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
    return render(request, "settings.html", {
        "tabs":tabs, 
        "active_tab_id":active_tab_id, 
        'page':tabs[active_tab_id][0], 
        'f':tabs[active_tab_id][1], 
        'apps':apps, 
        'active_side_id':-1
    })

@cal_time
@login_required
@bind_wx_check
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
            if isinstance(app_info, tuple):
                app_info[0].paginate(page=request.GET.get(app_info[0].prefix+"page",1), per_page=10)
                if app_info[1].prefix:
                    app_info[1].paginate(page=request.GET.get(app_info[1].prefix+"page",1), per_page=10)
            else:
                app_info.paginate(page=request.GET.get(app_info.prefix+"page",1), per_page=10)
            active_app = apps[i]
            active_app_specific= AppMgr.get_app_enable(apps[i].cast())
    logger.debug("active side id is %d" % active_side_id)

    tabs_names = get_tabs_names(request)
    tab_id = active_app.position
    #tab_id = tabs_names.index(active_app_specific.title)
    logger.debug("tab id is %d" % tab_id)

    return render(request, 'app.html', {'apps':apps, 'active_side_id':active_side_id, 'app_info':app_info, 'active_app':active_app, 'active_app_specific':active_app_specific, 'tab_id':tab_id})

@login_required
@page_verify('page_id')
def back_default(request, page_id):
    if page_id:
        page_id = int(page_id)
        tabs = get_tabs(request)
        active_tab_id = -1
        for tab in tabs:
            if tab[0].pk == page_id:
                active_tab_id = tab[0].position
                logger.debug("find form active tab id %d" % active_tab_id)
                break

        if active_tab_id == -1:
            return redirect('/settings')

        apps = get_apps(request)

        logger.debug("save page id %d" % page_id)
        page = get_object_or_404(Page, id = page_id)
        sub_page = page.cast()
        form = FormManager.get_form(sub_page, request)
        if request.method == 'POST':
            if form.is_valid():
                intropage = form.save(commit=False)
                intropage.title = get_default_title(sub_page)
                intropage.enable = True
                intropage.icon = get_default_icon(sub_page)
                intropage.save()
                return redirect("/settings/%d" % active_tab_id)
            else:
                logger.debug("form is not valid")
                return render(request, "settings.html", {"tabs":tabs, "active_tab_id":active_tab_id, 'page':sub_page, 'f':form, 'apps':apps, 'active_side_id':-1})
        else:
            return redirect("/settings/%d" % active_tab_id)
    else:
        logger.error("no page id")
    return redirect("/settings")

@login_required
@page_verify('page_id')
def save(request, page_id):
    if page_id is None:
        logger.error("no page id")
        return redirect("/settings")

    page_id = int(page_id)
    tabs = get_tabs(request)
    tabs_filtered = filter(lambda tab: tab[0].pk == page_id, tabs)
    active_tab_id = -1 if len(tabs_filtered) == 0 else tabs_filtered[0][0].position
    logger.debug("find form active tab id %d" % active_tab_id)

    if active_tab_id == -1:
        return redirect('/settings')

    if request.method == 'GET':
        return redirect("/settings/%d" % active_tab_id)

    logger.debug("save page id %d" % page_id)
    page = get_object_or_404(Page, id = page_id)
    sub_page = page.cast()
    enable = sub_page.enable
    form = FormManager.get_form(sub_page, request)
    print form
    if not form.is_valid():
        logger.error("form is not valid")
        apps = get_apps(request)
        return render(request, "settings.html", {"tabs":tabs, "active_tab_id":active_tab_id, 'page':sub_page, 'f':form, 'apps':apps, 'active_side_id':-1})

    page = form.save(commit=False)
    logger.debug("page is enable? " + str(enable))
    logger.debug("form.enable is? " + str(page.enable))
    if enable == page.enable:
        page.save()
        return redirect("/settings/%d" % active_tab_id)

    if enable:
        set_page_disabled(page)
    else:
        set_page_enable(page)

    return redirect("/settings/%d" % Page.objects.get(pk=page_id).position)

@login_required
@page_verify('page_id')
@transaction.commit_manually
def page_delete(request, page_id):
    page = get_object_or_404(Page, pk = page_id)
    cursor = connection.cursor()
    try:
        sql = 'update page set position = position - 1 where wx_id = %s and position > %s'
        cursor.execute(sql, (page.wx.pk, page.position))
        page.delete()
        #raise Exception()
    except Exception as e:
        transaction.rollback()
        logger.exception("page_delete error")
        raise e
    else:
        transaction.commit()
        return redirect("/settings")


@login_required
@contact_item_verify('item_id')
def add_edit_contact(request, item_id=None):
    if item_id:
        item = get_object_or_404(ContactItem, pk = item_id)
    else:
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
                max_pos = contact_app.contactitem_set.all().aggregate(Max('position'))
                position = int(max_pos['position__max'] or 0) + 1
                item.contact = contact_app
                item.position = position
            item.save()
            return render(request,'close_page.html')
    else:
        form = ContactItemForm(instance=item)

    return render(request, 'add_edit_contact.html', {'form':form, 'contact_id':item_id})

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
    id = item.contact_item.contact.pk
    item.delete()
    return redirect('/app/%d' % id)

@login_required
@join_item_verify('item_id')
def add_edit_join(request, item_id=None):
    if item_id:
        item = get_object_or_404(JoinItem, pk = item_id)
    else:
        item = None
    if request.method == 'POST':
        form = JoinItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
                join_app = JoinApp.objects.get(wx=wx)
                item.join = join_app
            item.pub_time = datetime.now()
            item.save()
            return render(request,'close_page.html')
    else:
        form = JoinItemForm(instance=item)

    return render(request, 'add_edit_join.html', {'form':form})

@login_required
@join_item_verify('item_id')
def join_delete(request, item_id):
    item = get_object_or_404(JoinItem, pk = item_id)
    app_id = item.join.pk
    item.delete()
    return redirect('/app/%d' % app_id)

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
                wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
                trends_app = TrendsApp.objects.get(wx=wx)
                max_pos = trends_app.trenditem_set.all().aggregate(Max('position'))
                position = int(max_pos['position__max'] or 0) + 1
                item.trend = trends_app
                item.position = position
            item.pub_time = datetime.now()
            item.save()
            return render(request,'close_page.html')
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
@team_item_verify('item_id')
def add_edit_team(request, item_id=None):
    if item_id:
        item = get_object_or_404(TeamItem, pk = item_id)
    else:
        peoples = None
        item = None
    if request.method == 'POST':
        form = TeamItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.pk is None:
                wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
                team_app = TeamApp.objects.get(wx=wx)
                max_pos = team_app.teamitem_set.all().aggregate(Max('position'))
                position = int(max_pos['position__max'] or 0) + 1
                item.team = team_app
                item.position = position
            item.pub_time = datetime.now()
            item.save()
            return render(request,'close_page.html')
    else:
        form = TeamItemForm(instance=item)

    return render(request, 'add_edit_team.html', {'form':form})

@login_required
@team_item_verify('item_id')
def team_delete(request, item_id):
    item = get_object_or_404(TeamItem, pk = item_id)
    app_id = item.team.pk
    item.delete()
    return redirect('/app/%d' % app_id)

@login_required
@page_verify('link_id')
@transaction.commit_manually
def add_edit_link_page(request, link_id=None):
    if link_id:
        item = get_object_or_404(LinkPage, pk = link_id)
    else:
        item = None

    if request.method == 'POST':
        form = LinkPageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                if item.pk is None:
                    wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
                    item.enable = True
                    item.wx = wx
                    ensure_new_page_position(item, wx)
                item.save()
                #raise Exception()
            except Exception as e:
                logger.exception("add_edit_link_page error")
                transaction.rollback()
                raise e
            else:
                transaction.commit()
                return render(request, 'close_page.html')
        else:
            logger.debug("form is not valid")
    else:
        form = LinkPageForm(instance=item)

    return render(request, 'add_edit_link.html', {'form':form})

@login_required
@page_verify('content_id')
@transaction.commit_manually
def add_edit_content_page(request, content_id=None):
    logger.debug("add edit content page")
    if content_id:
        item = get_object_or_404(ContentPage, pk = content_id)
    else:
        item = None

    if request.method == 'POST':
        form = ContentPageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                if item.pk is None:
                    wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
                    item.enable = True
                    item.wx = wx
                    ensure_new_page_position(item, wx)
                logger.debug("icon url %s" % item.icon.url)
                item.save()
                #raise Exception()
            except Exception as e:
                logger.exception("add_edit_content_page error")
                transaction.rollback()
                raise e
            else:
                transaction.commit()
                return render(request,'close_page.html')
        else:
            logger.debug("form is not valid")
    else:
        logger.debug("method is get")
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
                max_pos = case_app.caseitem_set.all().aggregate(Max('position'))
                position = int(max_pos['position__max'] or 0) + 1
                item.case_app= case_app
                item.position=position
            item.pub_time = datetime.now()
            logger.debug("item picurl %s" % item.case_pic1)
            item.save()
            return render(request,'close_page.html')
    else:
        form = CaseItemForm(instance=item)
    form.fields['cls'].queryset = CaseClass.objects.filter(case_app=case_app)

    return render(request, 'add_edit_case.html', {'form':form, 'item_id':item_id})

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
                max_pos = product_app.productitem_set.all().aggregate(Max('position'))
                position = int(max_pos['position__max'] or 0) + 1
                item.product_app = product_app
                item.position = position
            item.pub_time = datetime.now()
            item.save()
            return render(request,'close_page.html')
    else:
        form = ProductItemForm(instance=item)

    form.fields['cls'].queryset = ProductClass.objects.filter(product_app=product_app)

    return render(request, 'add_edit_product.html', {'form':form, 'item_id':item_id})

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

            cache.set('wx_access_token_%d' % wx_account.id, form.cleaned_data.get('access_token'), 7200)
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
        if request.method == "GET":
            menu_info = MenuTable(Menu.objects.filter(wx=wx_account))
            form = AddEditMenuForm()
            pages = Page.objects.filter(wx=wx_account)
            pages_id = []
            for page in pages:
                if not page.tab_name == u'首页':
                    subpage = page.cast()
                    if subpage.enable == True:
                        pages_id.append(page.id)
                else:
                    pages_id.append(page.id)
        return render(request, 'menu.html', {'apps' : apps, 'menu_info' : menu_info, 'form' : form, 'pages': pages})

@login_required
def menu_delete(request, menu_id):
    menu = get_object_or_404(Menu, pk = menu_id)
    menu.delete()
    return redirect('/menu')
