#coding: utf8
import logging
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from models import *
from framework.models import *
from forms import *
from django.contrib import auth
from siteviews import homepage_, intro_, business_, join_, help_, content_, trend_, team_, contact_, productitem_, product_, caseitem_, case_, joinitem_, trenditem_, teamitem_

logger = logging.getLogger('default')

def page(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    if page.real_type == ContentType.objects.get_for_model(HomePage):
        return homepage(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return intropage(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return businesspage(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return trend(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(TeamApp):
        return team(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(JoinApp):
        return join(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(ContactApp):
        return contact(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        return case(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        return product(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        return weibo(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(LinkPage):
        return link(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(ContentPage):
        return content(request, page_id)
    elif page.real_type == ContentType.objects.get_for_model(HelpPage):
        return helppage(request, page_id)

def deal_with_errors(form):
    msg = ''
    logger.debug(str(form.fields))
    for k,v in form.errors.iteritems():
        item = form.fields[k]
        if len(msg) > 0:
            msg += u'、'
        msg += item.label
    msg += u'</font>字段有错误'
    msg = '页面设置包含错误，目前无法预览<br/><br/><font color="red">' + msg + '<br/>请修正后再预览'
    return HttpResponse(msg)


def homepage(request, page_id):
    page = get_object_or_404(HomePage, pk=page_id)
    form = HomePageForm(request.POST, request.FILES, instance=page)
    if not form.is_valid():
        return deal_with_errors(form)

    homepage = form.save(commit=False)
    return homepage_(request, homepage)
def intropage(request, page_id):
    page = get_object_or_404(IntroPage, pk=page_id)
    form = IntroPageForm(request.POST, request.FILES, instance=page)
    if form.is_valid():
        intropage = form.save(commit=False)
        return intro_(request, intropage)
    else:
        return deal_with_errors(form)


def businesspage(request, page_id):
    page = get_object_or_404(BusinessPage, pk=page_id)
    form = BusinessPageForm(request.POST, request.FILES, instance=page)
    if form.is_valid():
        businesspage = form.save(commit=False)
        return business_(request, businesspage)
    else:
        return deal_with_errors(form)

def trend(request, page_id):
    app = get_object_or_404(TrendsApp, pk=page_id)
    form = TrendsAppForm(request.POST, request.FILES, instance=app)
    if form.is_valid():
        trendapp = form.save(commit=False)
        return trend_(request, app)
    else:
        return HttpResponse("%s" % str(form.errors))

def team(request, page_id):
    app = get_object_or_404(TeamApp, pk=page_id)
    form = TeamAppForm(request.POST, request.FILES, instance=app)
    if form.is_valid():
        teamapp = form.save(commit=False)
        return team_(request, app)
    else:
        return HttpResponse("%s" % str(form.errors))

def join(request, page_id):
    joinapp = get_object_or_404(JoinApp, pk=page_id)
    form = JoinAppForm(request.POST, request.FILES, instance=joinapp)
    if form.is_valid():
        joinapp = form.save(commit=False)
        return join_(request, joinapp)
    else:
        return deal_with_errors(form)

def contact(request, page_id):
    app = get_object_or_404(ContactApp, pk=page_id)
    form = ContactAppForm(request.POST, request.FILES, instance=app)
    if form.is_valid():
        app = form.save(commit=False)
        return contact_(request, app)
    else:
        return deal_with_errors(form)

def case(request, item_id):
    logger.debug("case %d" % int(item_id))
    caseapp = get_object_or_404(CaseApp, pk=item_id)
    form = CaseAppForm(request.POST, request.FILES, instance=caseapp)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        caseapp = form.save(commit=False)
        return case_(request, caseapp, None)


def product(request, item_id):
    logger.debug("preview product %d" % int(item_id))
    papp = get_object_or_404(ProductApp, pk=item_id)
    form = ProductAppForm(request.POST, request.FILES, instance=papp)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        papp = form.save(commit=False)
        return product_(request, papp, None)
def weibo(request, item_id):
    weibopage = get_object_or_404(WeiboPage, pk=item_id)
    form = WeiboPageForm(request.POST, request.FILES, instance=weibopage)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        weibopage = form.save(commit=False)
        return redirect(weibopage.url)

def link(request, item_id=None):
    if item_id:
        linkpage = get_object_or_404(LinkPage, pk=item_id)
    else:
        linkpage = None
    form = LinkPageForm(request.POST, request.FILES, instance=linkpage)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        linkpage = form.save(commit=False)
        wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
        linkpage.enable = True
        linkpage.wx = wx
        return redirect(linkpage.url)


def content(request, item_id = None):
    if item_id:
        content_page = get_object_or_404(ContentPage, pk=item_id)
        form = ContentPageForm(request.POST, request.FILES, instance=content_page)
    else:
        content_page = None
        form = ContentPageForm(request.POST, request.FILES, instance=content_page)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        content_page = form.save(commit=False)
        if content_page.pk is None:
            wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
            content_page.enable = True
            content_page.wx = wx

        return content_(request, content_page)

def helppage(request, item_id):
    page = get_object_or_404(HelpPage, pk=item_id)
    form = HelpPageForm(request.POST, request.FILES, instance=page)
    if form.is_valid():
        helppage = form.save(commit=False)
        return help_(request, helppage)
    else:
        return deal_with_errors(form)


def join_item(request):
    form = JoinItemForm(request.POST, request.FILES, instance=None)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        item = form.save(commit=False)
        if item.pk is None:
            user = auth.get_user(request)
            account = Account.objects.get(user=user)
            wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
            join_app = JoinApp.objects.get(wx=wx)
            item.join = join_app
        item.pub_time = datetime.now()
        return joinitem_(request, item)

def trend_item(request):
    form = TrendItemForm(request.POST, request.FILES, instance=None)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        item = form.save(commit=False)
        if item.pk is None:
            user = auth.get_user(request)
            account = Account.objects.get(user=user)
            wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
            trends_app = TrendsApp.objects.get(wx=wx)
            item.trend = trends_app
        item.pub_time = datetime.now()
        return trenditem_(request, item)

def team_item(request):
    form = TeamItemForm(request.POST, request.FILES, instance=None)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        item = form.save(commit=False)
        if item.pk is None:
            user = auth.get_user(request)
            account = Account.objects.get(user=user)
            wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
            team_app = TeamApp.objects.get(wx=wx)
            item.team = team_app
        item.pub_time = datetime.now()
        return teamitem_(request, item)

def case_item(request, item_id=None):
    if item_id:
        item = get_object_or_404(CaseItem, pk=item_id)
    else:
        item = None
    logger.debug("post %s" % str(request.POST))
    form = CaseItemForm(request.POST, request.FILES, instance=item)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        caseitem = form.save(commit=False)
        if caseitem.pk is None:
            wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
            case_app = CaseApp.objects.get(wx=wx)
            caseitem.case_app = case_app

        return caseitem_(request, caseitem)

def product_item(request, item_id=None):
    if item_id:
        item = get_object_or_404(ProductItem, pk=item_id)
    else:
        item = None
    form = ProductItemForm(request.POST, request.FILES, instance=item)
    if not form.is_valid():
        return deal_with_errors(form)
    else:
        pitem = form.save(commit=False)
        if pitem.pk is None:
            wx_account = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
            product_app = ProductApp.objects.get(wx=wx_account)
            pitem.product_app = product_app
        return productitem_(request, pitem)

