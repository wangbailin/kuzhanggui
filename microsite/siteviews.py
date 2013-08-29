#coding:utf-8
import logging

from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType

from rocket import settings
from models import *
logger = logging.getLogger('default')

def get_home_info(subpage):
    site_base_url = '/microsite'
    if subpage.real_type == ContentType.objects.get_for_model(IntroPage):
        return (site_base_url + "/intro/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/intro.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(BusinessPage):
        return (site_base_url + "/business/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/business.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(TrendsApp):
        return (site_base_url + "/trend/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/trend.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(JoinPage):
        return (site_base_url + "/join/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/joinus.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(ContactApp):
        return (site_base_url + "/contact/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/contact.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(WeiboPage):
        return (subpage.url, settings.STATIC_URL + "/siteicon/weibo.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(CaseApp):
        return (site_base_url + "/case/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/case.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(ProductApp):
        return (site_base_url + "/product/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/product.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(LinkPage):
        return (site_base_url + "/link/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/link.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(ContentPage):
        return (site_base_url + "/content/%d" % subpage.pk, subpage.icon.url, subpage._get_tab_name())

            
def homepage(request, item_id):
    homepage = get_object_or_404(HomePage, pk=item_id)
    pics = []
    if homepage.pic1:
        pics.append(homepage.pic1)
    if homepage.pic2:
        pics.append(homepage.pic2)
    if homepage.pic3:
        pics.append(homepage.pic3)
    if homepage.pic4:
        pics.append(homepage.pic4)
    logger.debug("%s" % str(pics))
    rows = []
    cols = []
    pages = Page.objects.filter(wx=homepage.wx)
    for p in pages:
        if p.real_type == homepage.real_type:
            continue
        if len(cols) >= 3:
            rows.append(cols)
            cols = []
        cols.append(get_home_info(p.cast()))
    if len(cols) > 0:
        rows.append(cols)
        cols = []
    return render(request, 'microsite/homepage.html', {'name':homepage.name, 'pics':pics, 'rows':rows})

def intro(request, item_id):
    intropage = get_object_or_404(IntroPage, pk=item_id)
    return render(request, 'microsite/intropage.html', {'title':intropage.title, 'content':intropage.content})

def business(request, item_id):
    business_page = get_object_or_404(BusinessPage, pk=item_id)
    return render(request, 'microsite/intropage.html', {'title':business_page.title, 'content':business_page.content})

def join(request, item_id):
    joinpage = get_object_or_404(JoinPage, pk=item_id)
    return render(request, 'microsite/intropage.html', {'title':joinpage.title, 'content':joinpage.content})

def content(request, item_id):
    content_page = get_object_or_404(ContentPage, pk=item_id)
    return render(request, 'microsite/intropage.html', {'title':content_page.title, 'content':content_page.content})

def weibo(request, item_id):
    weibopage = get_object_or_404(WeiboPage, pk=item_id)
    return render(request, 'microsite/weibopage.html', {'title':weibopage.title, 'url':weibopage.url})

def trend(request, item_id):
    trendapp = get_object_or_404(TrendsApp, pk=item_id)
    trenditems = TrendItem.objects.filter(trend=trendapp)
    items = []
    for i in trenditems:
        logger.debug("one trend title %s" % i.title)
        items.append( (i.title, '/microsite/trenditem/%d' % i.pk) )
    return render(request, 'microsite/trendapp.html', {'title':trendapp._get_tab_name(), 'items':items})

def trenditem(request, item_id):
    trenditem = get_object_or_404(TrendItem, pk=item_id)
    logger.debug("content %s" % trenditem.content)
    return render(request, 'microsite/trenditem.html', {'title':trenditem.title, 'content':trenditem.content.encode("utf8")})

def case(request, item_id, class_id=None):
    empty_msg = u'没有案例'
    logger.debug("case %d" % int(item_id))
    caseapp = get_object_or_404(CaseApp, pk=item_id)
    caseclasses = CaseClass.objects.filter(case_app=caseapp)
    if class_id:
        caseclass = get_object_or_404(CaseClass, pk=class_id)
    else:
        if len(caseclasses) == 0:
            return render(request, 'microsite/message.html', {'title':caseapp._get_tab_name(), 'message':empty_msg})
        else:
            caseclass = caseclasses[0]
            
    caseitems = CaseItem.objects.filter(cls=caseclass)
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
        items.append( (ci, pic_url.url) )
        if len(items) >=2 :
            rows.append(items)
            items = []
    if len(items) > 0:
        rows.append(items)
    return render(request, 'microsite/caseapp.html', {'title':caseapp._get_tab_name(), 'rows':rows, 'caseclass':caseclass, 'caseclasses':caseclasses})

def caseitem(request, item_id):
    logger.debug("caseitem %d", item_id)
    caseitem = get_object_or_404(CaseItem, pk=item_id)
    pics = []
    if caseitem.case_pic1:
        pics.append(caseitem.case_pic1)
    if caseitem.case_pic2:
        pics.append(caseitem.case_pic2)
    if caseitem.case_pic3:
        pics.append(caseitem.case_pic3)
    if caseitem.case_pic4:
        pics.append(caseitem.case_pic4)

    return render(request, 'microsite/caseitem.html', {'title':caseitem.title, 'pics':pics, 'intro':caseitem.case_intro})

def link(request, item_id):
    logger.debug("link %d" % int(item_id))
    linkpage = get_object_or_404(LinkPage, pk=item_id)
    return render(request, 'microsite/linkpage.html', {'title':linkpage.title, 'url':linkpage.url})


def product(request, item_id, class_id=None):
    empty_msg = u'没有产品'
    logger.debug("product %d" % int(item_id))
    papp = get_object_or_404(ProductApp, pk=item_id)
    pclasses = ProductClass.objects.filter(product_app=papp)
    if class_id:
        pclass = get_object_or_404(ProductClass, pk=class_id)
    else:
        if len(pclasses) == 0:
            return render(request, 'microsite/message.html', {'title':papp._get_tab_name(), 'message':empty_msg})
        pclass = pclasses[0]
    pitems = ProductItem.objects.filter(cls=pclass)
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
        items.append( (p, pic_url.url) )
    return render(request, 'microsite/productapp.html', {'title':papp._get_tab_name(), 'items':items, 'pclass':pclass, 'pclasses':pclasses})

def product_item(request, item_id):
    logger.debug("product item %d", item_id)
    pitem = get_object_or_404(ProductItem, pk=item_id)
    pics = []
    if pitem.product_pic1:
        pics.append(pitem.product_pic1)
    if pitem.product_pic2:
        pics.append(pitem.product_pic2)
    if pitem.product_pic3:
        pics.append(pitem.product_pic3)
    if pitem.product_pic4:
        pics.append(pitem.product_pic4)

    return render(request, 'microsite/product_item.html', {'title':pitem.title, 'pics':pics, 'intro':pitem.product_intro})
    

def contact(request, item_id):
    logger.debug("contact app %d" % int(item_id))
    app = get_object_or_404(ContactApp, pk=item_id)
    items = ContactItem.objects.filter(contact=app)
    infos = []
    for item in items:
        contact_peoples = ContactPeople.objects.filter(contact_item=item)
        infos.append( (item, contact_peoples) )
    return render(request, 'microsite/contact_app.html', {'title':app._get_tab_name(), 'infos':infos})


