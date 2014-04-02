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


def get_footer(id):
    try:
        page = get_object_or_404(Page, pk=id)
        homepage = ContentType.objects.get_for_model(HomePage).get_object_for_this_type(wx=page.wx)
    except:
        return None
    return homepage.pk


def homepage_(request, homepage):
    pics = []
    exps = []
    if homepage.pic1:
        pics.append((homepage.pic1, homepage.exp1, homepage.link1))
    if homepage.pic2:
        pics.append((homepage.pic2, homepage.exp2, homepage.link2))
    if homepage.pic3:
        pics.append((homepage.pic3, homepage.exp3, homepage.link3))
    if homepage.pic4:
        pics.append((homepage.pic4, homepage.exp4, homepage.link4))
    logger.debug("%s" % str(pics))
    rows = []
    items = []
    pages = Page.objects.filter(wx=homepage.wx, enable=True).order_by("position")
    for p in pages:
        if p.real_type == homepage.real_type:
            continue
        if len(items) >= 3:
            rows.append(items)
            items = []
        subp = p.cast()
        if subp.real_type == ContentType.objects.get_for_model(WeiboPage) or \
            subp.real_type == ContentType.objects.get_for_model(LinkPage):
            items.append((subp.url, subp._get_icon(), subp._get_tab_name()))
        else:
            server = "http://" + request.META["HTTP_HOST"] 
            items.append((server + get_page_url(subp), subp._get_icon(), subp._get_tab_name()))

    if len(items) > 0:
        rows.append(items)

    return render(request, 'microsite/homepage.html', {'name':homepage.name, 'pics':pics, 'rows':rows, 'theme': site_templates[homepage.wx.wsite_template].site_template})


@cal_time
@sts_decorate
def homepage(request, item_id):
    homepage = get_object_or_404(HomePage, pk=item_id)
    return homepage_(request, homepage)

def intro_(request, intropage):
    homepage_id=get_footer(intropage.pk)
    return render(request, 'microsite/contentpage.html', {'title':intropage.title, 'content':intropage.content, 'homepage_id':homepage_id, 'theme': site_templates[intropage.wx.wsite_template].site_template})
def intro(request, item_id):
    intropage = get_object_or_404(IntroPage, pk=item_id)
    return intro_(request, intropage)

def business_(request, business_page):
    homepage_id=get_footer(business_page)
    return render(request, 'microsite/contentpage.html', {'title':business_page.title, 'content':business_page.content, 'homepage_id':homepage_id, 'theme': site_templates[business_page.wx.wsite_template].site_template})

def business(request, item_id):
    business_page = get_object_or_404(BusinessPage, pk=item_id)
    return business_(request, business_page)

def join_(request, joinapp):
    homepage_id=get_footer(joinapp.pk)
    joinitems = JoinItem.objects.filter(join=joinapp, publish=True).order_by("-position")
    pic_url = "http://" + request.META["HTTP_HOST"] + settings.STATIC_URL + consts.DEFAULT_JOIN_COVER
    if joinapp.pic:
        pic_url = "http://" + request.META["HTTP_HOST"] + joinapp.pic.url
    items = []
    for i in joinitems:
        logger.debug("one join job title %s" % i.job_title)
        items.append( (i.job_title, '/microsite/joinitem/%d' % i.pk, i.number, i.pub_time))
    return render(request, 'microsite/joinapp.html', {'title':joinapp._get_tab_name(), 'pic_url':pic_url, 'front_words':joinapp.front_words, 'contact':joinapp.contact, 'end_words':joinapp.end_words, 'items':items,'homepage_id':homepage_id, 'theme': site_templates[joinapp.wx.wsite_template].site_template})
def join(request, item_id):
    joinapp = get_object_or_404(JoinApp, pk=item_id)
    return join_(request, joinapp)

def help_(request, helppage):
    homepage_id=get_footer(helppage.pk)
    return render(request, 'microsite/contentpage.html', {'title':helppage.title, 'content':helppage.content, 'homepage_id':homepage_id, 'theme': site_templates[helppage.wx.wsite_template].site_template})

def help(request, item_id):
    helppage = get_object_or_404(HelpPage, pk=item_id)
    return help_(request, helppage)

def content_(request, content_page):
    homepage_id=get_footer(content_page.pk)
    return render(request, 'microsite/contentpage.html', {'title':content_page.title, 'content':content_page.content, 'homepage_id':homepage_id, 'theme': site_templates[content_page.wx.wsite_template].site_template})
def content(request, item_id):
    content_page = get_object_or_404(ContentPage, pk=item_id)
    return content_(request, content_page)

def weibo_(request, weibopage):
    return render(request, 'microsite/weibopage.html', {'title':weibopage.title, 'url':weibopage.url})

def weibo(request, item_id):
    weibopage = get_object_or_404(WeiboPage, pk=item_id)
    return weibo_(request, weibopage)

def trend_(request, trendapp):
    homepage_id=get_footer(trendapp)
    trenditems = TrendItem.objects.filter(trend=trendapp).order_by("-position")
    items = []
    for i in trenditems:
        logger.debug("one trend title %s" % i.title)
        cover_url = "http://" + request.META["HTTP_HOST"] + settings.STATIC_URL + consts.DEFAULT_TRENDITEM_COVER
        if i.cover:
            cover_url = "http://" + request.META["HTTP_HOST"] + i.cover.url
        new = (datetime.date.today() - i.pub_time.date()) <= datetime.timedelta(days=7)
        items.append( (i.title, '/microsite/trenditem/%d' % i.pk, i.pub_time, new, cover_url, i.summary))
    return render(request, 'microsite/trendapp.html', {'title':trendapp._get_tab_name(), 'items':items, 'homepage_id':homepage_id, 'theme': site_templates[trendapp.wx.wsite_template].site_template})
def trend(request, item_id):
    trendapp = get_object_or_404(TrendsApp, pk=item_id)
    return trend_(request, trendapp)

def team_(request, teamapp):
    homepage_id=get_footer(teamapp.pk)
    teamitems = TeamItem.objects.filter(team=teamapp).order_by("position")
    items = []
    for i in teamitems:
        logger.debug("one team name %s" % i.name)
        picture_url = i.picture.url
        items.append( (i.name, '/microsite/teamitem/%d' % i.pk, i.job_title, picture_url, i.person_digest))
    return render(request, 'microsite/teamapp.html', {'title':teamapp._get_tab_name(), 'items':items, 'homepage_id':homepage_id, 'theme': site_templates[teamapp.wx.wsite_template].site_template})
def team(request, item_id):
    teamapp = get_object_or_404(TeamApp, pk=item_id)
    return team_(request, teamapp)

def joinitem_(request, joinitem):
    contents = []
    requires = []
    if joinitem.content1:
        contents.append(joinitem.content1)
    if joinitem.content2:
        contents.append(joinitem.content2)
    if joinitem.content3:
        contents.append(joinitem.content3)
    if joinitem.content4:
        contents.append(joinitem.content4)
    logger.debug("%s" % str(contents))
    if joinitem.require1:
        requires.append(joinitem.require1)
    if joinitem.require2:
        requires.append(joinitem.require2)
    if joinitem.require3:
        requires.append(joinitem.require3)
    if joinitem.require4:
        requires.append(joinitem.require4)
    logger.debug("%s" % str(requires))
    homepage_id=get_footer(joinitem.join.pk)
    return render(request, 'microsite/joinitempage.html', {'job_title':joinitem.job_title, 'number':joinitem.number, 'pub_time': joinitem.pub_time, 'contents':contents, 'requires':requires, 'homepage_id':homepage_id, 'theme': site_templates[joinitem.join.wx.wsite_template].site_template})
def joinitem(request, item_id):
    joinitem = get_object_or_404(JoinItem, pk=item_id)
    logger.debug("content %s %s %s %s" % (joinitem.content1, joinitem.content2, joinitem.content3, joinitem.content4))
    return joinitem_(request, joinitem)

def trenditem_(request, trenditem):
    homepage_id=get_footer(trenditem.trend.pk)
    return render(request, 'microsite/contentpage.html', {'title':trenditem.title, 'content':trenditem.content.encode("utf8"), 'homepage_id':homepage_id, 'theme': site_templates[trenditem.trend.wx.wsite_template].site_template})
def trenditem(request, item_id):
    trenditem = get_object_or_404(TrendItem, pk=item_id)
    logger.debug("content %s" % trenditem.content)
    return trenditem_(request, trenditem)

def teamitem_(request, teamitem):
    homepage_id=get_footer(teamitem.team.pk)
    picture_url = teamitem.picture.url
    item = (teamitem.name, '/microsite/teamitem/%s' % teamitem.id, teamitem.job_title, picture_url, teamitem.person_digest)
    return render(request, 'microsite/teamitempage.html', {'title':teamitem.name, 'item':item, 'content':teamitem.person_content.encode("utf8"), 'homepage_id':homepage_id, 'theme': site_templates[teamitem.team.wx.wsite_template].site_template})
def teamitem(request, item_id):
    teamitem = get_object_or_404(TeamItem, pk=item_id)
    logger.debug("content %s" % teamitem.person_content)
    return teamitem_(request, teamitem)

def case_(request, caseapp, class_id):
    homepage_id=get_footer(caseapp.pk)
    caseclasses = CaseClass.objects.filter(case_app=caseapp).order_by("-position")

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

    return render(request, 'microsite/caseapp.html', {'title':caseapp._get_tab_name(), 'rows':rows, 'caseclass':caseclass, 'caseclasses':caseclasses, 'app':caseapp, 'homepage_id':homepage_id, 'theme': site_templates[caseapp.wx.wsite_template].site_template})


def case(request, item_id, class_id=None):
    logger.debug("case %d" % int(item_id))
    caseapp = get_object_or_404(CaseApp, pk=item_id)
    return case_(request, caseapp, class_id)

def caseitem_(request, caseitem):
    homepage_id=get_footer(caseitem.case_app.pk)
    pics = []
    if caseitem.case_pic1:
        pics.append(caseitem.case_pic1.url)
    if caseitem.case_pic2:
        pics.append(caseitem.case_pic2.url)
    if caseitem.case_pic3:
        pics.append(caseitem.case_pic3.url)
    if caseitem.case_pic4:
        pics.append(caseitem.case_pic4.url)

    return render(request, 'microsite/item.html', {'title':caseitem.title, 'pics':pics, 'intro':caseitem.case_intro, 'homepage_id':homepage_id, 'theme': site_templates[caseitem.case_app.wx.wsite_template].site_template})


def caseitem(request, item_id):
    logger.debug("caseitem %d", item_id)
    caseitem = get_object_or_404(CaseItem, pk=item_id)
    return caseitem_(request, caseitem)

def product_(request, papp, class_id):
    homepage_id=get_footer(papp.pk)
    pclasses = ProductClass.objects.filter(product_app=papp).order_by("-position")
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

    return render(request, 'microsite/productapp.html', {'title':papp._get_tab_name(), 'rows':rows, 'pclass':pclass, 'pclasses':pclasses, 'app' : papp, 'homepage_id':homepage_id, 'theme': site_templates[papp.wx.wsite_template].site_template})


def product(request, item_id, class_id=None):
    logger.debug("product %d" % int(item_id))
    papp = get_object_or_404(ProductApp, pk=item_id)
    return product_(request, papp, class_id)

def productitem_(request, pitem):
    homepage_id=get_footer(pitem.product_app.pk)
    pics = []
    if pitem.product_pic1:
        pics.append(pitem.product_pic1.url)
    if pitem.product_pic2:
        pics.append(pitem.product_pic2.url)
    if pitem.product_pic3:
        pics.append(pitem.product_pic3.url)
    if pitem.product_pic4:
        pics.append(pitem.product_pic4.url)

    return render(request, 'microsite/item.html', {'title':pitem.title, 'pics':pics, 'intro':pitem.product_intro, 'homepage_id':homepage_id, 'theme': site_templates[pitem.product_app.wx.wsite_template].site_template})


def productitem(request, item_id):
    logger.debug("product item %d", item_id)
    pitem = get_object_or_404(ProductItem, pk=item_id)
    return productitem_(request, pitem)

def contact_(request, app):
    homepage_id=get_footer(app.pk)
    items = ContactItem.objects.filter(contact=app).order_by("-position")
    infos = []
    for item in items:
        contact_peoples = ContactPeople.objects.filter(contact_item=item)
        infos.append( (item, contact_peoples) )
    return render(request, 'microsite/contactapp.html', {'title':app._get_tab_name(), 'infos':infos, 'homepage_id':homepage_id, 'theme': site_templates[app.wx.wsite_template].site_template})


def contact(request, item_id):
    logger.debug("contact app %d" % int(item_id))
    app = get_object_or_404(ContactApp, pk=item_id)
    return contact_(request, app)

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

def pic(request):
    return render(request, 'microsite/pic.html', {'title':request.GET['title'], 'path' : request.GET['p'], 'theme': request.GET['t']});


def contact_map(request, item_id, cur_lat, cur_lng):
    logger.debug("contact item %d" % int(item_id))
    item = get_object_or_404(ContactItem, pk=item_id)
    try:
        people = ContactPeople.objects.get(contact_item=item)
    except ObjectDoesNotExist:
        people = None

    return render(request, 'microsite/contactmap.html', {'item':item, 'people':people, 'cur_lat':cur_lat, 'cur_lng': cur_lng, 'theme': site_templates[item.contact.wx.wsite_template].site_template})
