#coding:utf-8
import logging

from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
import datetime

from rocket import settings
from models import *
from microsite import consts
from framework.models import Account, WXAccount
from site_template import site_templates
logger = logging.getLogger('default')
sts_logger = logging.getLogger('sts')
from wx_match import cal_time, sts_decorate

def get_home_info(subpage):
    if subpage.real_type == ContentType.objects.get_for_model(WeiboPage) or subpage.real_type == ContentType.objects.get_for_model(LinkPage):
        return (subpage.url, subpage._get_icon(), subpage._get_tab_name())
    else:
        return (get_page_url(subpage), subpage._get_icon(), subpage._get_tab_name())

def homepage_(request, homepage):
    pics = []
    exps = []
    if homepage.pic1:
        pics.append((homepage.pic1, homepage.exp1))
    if homepage.pic2:
        pics.append((homepage.pic2, homepage.exp2))
    if homepage.pic3:
        pics.append((homepage.pic3, homepage.exp3))
    if homepage.pic4:
        pics.append((homepage.pic4, homepage.exp4))
    logger.debug("%s" % str(pics))
    rows = []
    items = []
    pages = Page.objects.filter(wx=homepage.wx)
    for p in pages:
        if p.real_type == homepage.real_type:
            continue
        subp = p.cast()
        if not page_is_enable(subp):
            continue
        if len(items) >= 3:
            rows.append(items)
            items = []
        items.append(get_home_info(subp))
    if len(items) > 0:
        rows.append(items)

    return render(request, 'microsite/homepage.html', {'name':homepage.name, 'pics':pics, 'rows':rows, 'theme': site_templates[homepage.wx.wsite_template].site_template})


@cal_time            
@sts_decorate
def homepage(request, item_id):
    homepage = get_object_or_404(HomePage, pk=item_id)
    return homepage_(request, homepage)
    
def intro_(request, intropage):
    return render(request, 'microsite/contentpage.html', {'title':intropage.title, 'content':intropage.content, 'theme': site_templates[intropage.wx.wsite_template].site_template})
@sts_decorate
def intro(request, item_id):
    intropage = get_object_or_404(IntroPage, pk=item_id)
    return intro_(request, intropage)

def business_(request, business_page):
    return render(request, 'microsite/contentpage.html', {'title':business_page.title, 'content':business_page.content, 'theme': site_templates[business_page.wx.wsite_template].site_template})
    
@sts_decorate
def business(request, item_id):
    business_page = get_object_or_404(BusinessPage, pk=item_id)
    return business_(request, business_page)

def join_(request, joinpage):
    return render(request, 'microsite/contentpage.html', {'title':joinpage.title, 'content':joinpage.content, 'theme': site_templates[joinpage.wx.wsite_template].site_template})
    
@sts_decorate
def join(request, item_id):
    joinpage = get_object_or_404(JoinPage, pk=item_id)
    return join_(request, joinpage)

def help_(request, helppage):
    return render(request, 'microsite/contentpage.html', {'title':helppage.title, 'content':helppage.content, 'theme': site_templates[helppage.wx.wsite_template].site_template})

@sts_decorate
def help(request, item_id):
    helppage = get_object_or_404(HelpPage, pk=item_id)
    return help_(request, helppage)

def content_(request, content_page):
    return render(request, 'microsite/contentpage.html', {'title':content_page.title, 'content':content_page.content, 'theme': site_templates[content_page.wx.wsite_template].site_template})
@sts_decorate
def content(request, item_id):
    content_page = get_object_or_404(ContentPage, pk=item_id)
    return content_(request, content_page)

def weibo_(request, weibopage):
    return render(request, 'microsite/weibopage.html', {'title':weibopage.title, 'url':weibopage.url})

@sts_decorate
def weibo(request, item_id):
    weibopage = get_object_or_404(WeiboPage, pk=item_id)
    return weibo_(request, weibopage)

def trend_(request, trendapp):
    trenditems = TrendItem.objects.filter(trend=trendapp).order_by("-pub_time")
    items = []
    for i in trenditems:
        logger.debug("one trend title %s" % i.title)
        cover_url = settings.SITE_URL + settings.STATIC_URL + consts.DEFAULT_TRENDITEM_COVER
        if i.cover:
            cover_url = i.cover.url
        new = (datetime.date.today() - i.pub_time) <= datetime.timedelta(days=7)
        items.append( (i.title, '/microsite/trenditem/%d' % i.pk, i.pub_time, new, cover_url, i.summary))
    return render(request, 'microsite/trendapp.html', {'title':trendapp._get_tab_name(), 'items':items, 'theme': site_templates[trendapp.wx.wsite_template].site_template})
@sts_decorate
def trend(request, item_id):
    trendapp = get_object_or_404(TrendsApp, pk=item_id)
    return trend_(request, trendapp)

def team_(request, teamapp):
    teamitems = TeamItem.objects.filter(team=teamapp).order_by("-pub_time")
    items = []
    for i in teamitems:
        logger.debug("one team title %s" % i.title)
        cover_url = settings.SITE_URL + settings.STATIC_URL + consts.DEFAULT_TEAMITEM_COVER
        if i.cover:
            cover_url = i.cover.url
        new = (datetime.date.today() - i.pub_time) <= datetime.timedelta(days=7)
        items.append( (i.title, '/microsite/teamitem/%d' % i.pk, i.pub_time, new, cover_url, i.summary))
    return render(request, 'microsite/teamapp.html', {'title':teamapp._get_tab_name(), 'items':items, 'theme': site_templates[teamapp.wx.wsite_template].site_template})
@sts_decorate
def team(request, item_id):
    teamapp = get_object_or_404(TeamApp, pk=item_id)
    return team_(request, teamapp)

def trenditem_(request, trenditem):
    return render(request, 'microsite/contentpage.html', {'title':trenditem.title, 'content':trenditem.content.encode("utf8"), 'theme': site_templates[trenditem.trend.wx.wsite_template].site_template})
@sts_decorate
def trenditem(request, item_id):
    trenditem = get_object_or_404(TrendItem, pk=item_id)
    logger.debug("content %s" % trenditem.content)
    return trenditem_(request, trenditem)

def teamitem_(request, teamitem):
    return render(request, 'microsite/contentpage.html', {'title':teamitem.name, 'content':teamitem.person_content.encode("utf8"), 'theme': site_templates[teamitem.team.wx.wsite_template].site_template})
@sts_decorate
def teamitem(request, item_id):
    teamitem = get_object_or_404(TeamItem, pk=item_id)
    logger.debug("content %s" % teamitem.content)
    return teamitem_(request, teamitem)

def case_(request, caseapp, class_id):
    caseclasses = CaseClass.objects.filter(case_app=caseapp)
    
    if class_id:
        caseclass = get_object_or_404(CaseClass, pk=class_id)
    else:
        caseclass = None
    
    if caseclass is not None:
        caseitems = CaseItem.objects.filter(cls=caseclass)
    else:
        caseitems = caseapp.caseitem_set.all()

    rows = []
    items = []
    for ci in caseitems:
        pic_url = ''
        if ci.case_pic1:
            pic_url = ci.case_pic1
        elif ci.case_pic2:
            pic_url = ci.case_pic2
        elif ci.case_pic3:
            pic_url = ci.case_pic3
        elif ci.case_pic4:
            pic_url = ci.case_pic4
        
        if len(items) >= 2:
            rows.append(items)
            items = []
        items.append( (ci, pic_url.url) )

    if len(items) > 0:
        rows.append(items)

    return render(request, 'microsite/caseapp.html', {'title':caseapp._get_tab_name(), 'rows':rows, 'caseclass':caseclass, 'caseclasses':caseclasses, 'app':caseapp, 'theme': site_templates[caseapp.wx.wsite_template].site_template})


@sts_decorate
def case(request, item_id, class_id=None):
    logger.debug("case %d" % int(item_id))
    caseapp = get_object_or_404(CaseApp, pk=item_id)
    return case_(request, caseapp, class_id)

def caseitem_(request, caseitem):
    pics = []
    if caseitem.case_pic1:
        pics.append(caseitem.case_pic1)
    if caseitem.case_pic2:
        pics.append(caseitem.case_pic2)
    if caseitem.case_pic3:
        pics.append(caseitem.case_pic3)
    if caseitem.case_pic4:
        pics.append(caseitem.case_pic4)

    return render(request, 'microsite/item.html', {'title':caseitem.title, 'pics':pics, 'intro':caseitem.case_intro, 'theme': site_templates[caseitem.case_app.wx.wsite_template].site_template})


@sts_decorate
def caseitem(request, item_id):
    logger.debug("caseitem %d", item_id)
    caseitem = get_object_or_404(CaseItem, pk=item_id)
    return caseitem_(request, caseitem)

def product_(request, papp, class_id):
    pclasses = ProductClass.objects.filter(product_app=papp)
    if class_id:
        pclass = get_object_or_404(ProductClass, pk=class_id)
    else:
        pclass = None

    if pclass is not None:
        pitems = ProductItem.objects.filter(cls=pclass)
    else:
        pitems = papp.productitem_set.all()

    rows = []
    items = []
    for p in pitems:
        pic_url = ''
        if p.product_pic1:
            pic_url = p.product_pic1
        elif ci.product_pic2:
            pic_url = p.product_pic2
        elif ci.product_pic3:
            pic_url = p.product_pic3
        elif ci.product_pic4:
            pic_url = p.product_pic4

        if len(items) >= 2:
            rows.append(items)
            items = []
        items.append( (p, pic_url.url) )

    if len(items) > 0:
        rows.append(items)

    return render(request, 'microsite/productapp.html', {'title':papp._get_tab_name(), 'rows':rows, 'pclass':pclass, 'pclasses':pclasses, 'app' : papp, 'theme': site_templates[papp.wx.wsite_template].site_template})


@sts_decorate
def product(request, item_id, class_id=None):
    logger.debug("product %d" % int(item_id))
    papp = get_object_or_404(ProductApp, pk=item_id)
    return product_(request, papp, class_id)

def productitem_(request, pitem):
    pics = []
    if pitem.product_pic1:
        pics.append(pitem.product_pic1)
    if pitem.product_pic2:
        pics.append(pitem.product_pic2)
    if pitem.product_pic3:
        pics.append(pitem.product_pic3)
    if pitem.product_pic4:
        pics.append(pitem.product_pic4)

    return render(request, 'microsite/item.html', {'title':pitem.title, 'pics':pics, 'intro':pitem.product_intro, 'theme': site_templates[pitem.product_app.wx.wsite_template].site_template})
    

@sts_decorate
def productitem(request, item_id):
    logger.debug("product item %d", item_id)
    pitem = get_object_or_404(ProductItem, pk=item_id)
    return productitem_(request, pitem)

def contact_(request, app):
    items = ContactItem.objects.filter(contact=app)
    infos = []
    for item in items:
        contact_peoples = ContactPeople.objects.filter(contact_item=item)
        infos.append( (item, contact_peoples) )
    return render(request, 'microsite/contactapp.html', {'title':app._get_tab_name(), 'infos':infos, 'theme': site_templates[app.wx.wsite_template].site_template})


@sts_decorate
def contact(request, item_id):
    logger.debug("contact app %d" % int(item_id))
    app = get_object_or_404(ContactApp, pk=item_id)
    return contact_(request, app)

@sts_decorate
def telephone(request, item_id):
    logger.debug("contact app %d" % int(item_id))
    app = get_object_or_404(ContactApp, pk=item_id)
    items = ContactItem.objects.filter(contact=app)
    infos = []
    for item in items:
        contact_peoples = ContactPeople.objects.filter(contact_item=item)
        if contact_peoples.count() > 0:
            infos.append( (item, contact_peoples) )
    return render(request, 'microsite/telephone.html', {'title':app._get_tab_name(), 'infos':infos, 'theme': site_templates[app.wx.wsite_template].site_template})

@sts_decorate
def pic(request):
    return render(request, 'microsite/pic.html', {'title':request.GET['title'], 'path' : request.GET['p'], 'theme': request.GET['t']});


@sts_decorate
def contact_map(request, item_id, cur_lat, cur_lng):
    logger.debug("contact item %d" % int(item_id))
    item = get_object_or_404(ContactItem, pk=item_id)
    try:
        people = ContactPeople.objects.get(contact_item=item)
    except ObjectDoesNotExist:
        people = None

    return render(request, 'microsite/contactmap.html', {'item':item, 'people':people, 'cur_lat':cur_lat, 'cur_lng': cur_lng, 'theme': site_templates[item.contact.wx.wsite_template].site_template})
