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
        return (site_base_url + "/weibo/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/weibo.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(CaseApp):
        return (site_base_url + "/case/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/case.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(ProductApp):
        return (site_base_url + "/product/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/product.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(LinkPage):
        return (site_base_url + "/link/%d" % subpage.pk, settings.STATIC_URL + "/siteicon/link.gif", subpage._get_tab_name())
    elif subpage.real_type == ContentType.objects.get_for_model(ContentPage):
        return (site_base_url + "/content/%d" % subpage.pk, settings.MEDIA_URL + subpage.icon, subpage._get_tab_name())

            
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
