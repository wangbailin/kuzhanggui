#coding: utf8
import logging
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from models import *
from forms import *
from siteviews import get_home_info

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
    elif page.real_type == ContentType.objects.get_for_model(JoinPage):
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
    items = []
    pages = Page.objects.filter(wx=homepage.wx)
    for p in pages:
        if p.real_type == homepage.real_type:
            continue
        items.append(get_home_info(p.cast()))

    return render(request, 'microsite/homepage.html', {'name':homepage.name, 'pics':pics, 'items':items})

def intropage(request, page_id):
    page = get_object_or_404(IntroPage, pk=page_id)
    form = IntroPageForm(request.POST, request.FILES, instance=page)
    if form.is_valid():
        intropage = form.save(commit=False)
        return render(request, 'microsite/contentpage.html', {'title':intropage.title, 'content':intropage.content})
    else:
        return deal_with_errors(form)        


def businesspage(request, page_id):
    page = get_object_or_404(BusinessPage, pk=page_id)
    form = BusinessPageForm(request.POST, request.FILES, instance=page)
    if form.is_valid():
        businesspage = form.save(commit=False)
        return render(request, 'microsite/contentpage.html', {'tilte':businesspage.title, 'content':businesspage.content})
    else:
        return deal_with_errors(form)        

def trend(request, page_id):
    app = get_object_or_404(TrendsApp, pk=page_id)
    form = TrendsAppForm(request.POST, request.FILES, instance=app)
    if form.is_valid():
        trendapp = form.save(commit=False)
        trenditems = TrendItem.objects.filter(trend=trendapp).order_by("-pub_time")
        items = []
        for i in trenditems:
            logger.debug("one trend title %s" % i.title)
            items.append( (i.title, '/microsite/trenditem/%d' % i.pk, i.pub_time, True, 'http://r.limijiaoyin.com/media/ckeditor/2013/08/30/weixinapp2.png') )
        return render(request, 'microsite/trendapp.html', {'title':trendapp._get_tab_name(), 'items':items})
    else:
        return HttpResponse("%s" % str(form.errors))

def join(request, page_id):
    joinpage = get_object_or_404(JoinPage, pk=page_id)
    form = JoinPageForm(request.POST, request.FILES, instance=joinpage)
    if form.is_valid():
        joinpage = form.save(commit=False)
        return render(request, 'microsite/contentpage.html', {'title':joinpage.title, 'content':joinpage.content})
    else:
        return deal_with_errors(form)        

def contact(request, page_id):
    app = get_object_or_404(ContactApp, pk=page_id)
    form = ContactAppForm(request.POST, request.FILES, instance=app)
    if form.is_valid():
        app = form.save(commit=False)
        items = ContactItem.objects.filter(contact=app)
        infos = []
        for item in items:
            contact_peoples = ContactPeople.objects.filter(contact_item=item)
            infos.append( (item, contact_peoples) )
        return render(request, 'microsite/contactapp.html', {'title':app._get_tab_name(), 'infos':infos})
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
        caseclasses = CaseClass.objects.filter(case_app=caseapp)
        
        if len(caseclasses) == 0:
            caseclass = None
        else:
            caseclass = caseclasses[0]
        
        if caseclass is not None:
            caseitems = CaseItem.objects.filter(cls=caseclass)
        else:
            caseitems = []

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

        return render(request, 'microsite/caseapp.html', {'title':caseapp._get_tab_name(), 'rows':rows, 'caseclass':caseclass, 'caseclasses':caseclasses})


def product(request, item_id):
    logger.debug("preview product %d" % int(item_id))
    papp = get_object_or_404(ProductApp, pk=item_id)
    form = ProductAppForm(request.POST, request.FILES, instance=papp)
    if not form.is_valid():
        return deal_with_errors(form)        
    else:
        papp = form.save(commit=False)
        pclasses = ProductClass.objects.filter(product_app=papp)
        if class_id:
            pclass = get_object_or_404(ProductClass, pk=class_id)
        else:
            if len(pclasses) == 0:
                pclass = None
            else:
                pclass = pclasses[0]

        if pclass is not None:
            pitems = ProductItem.objects.filter(cls=pclass)
        else:
            pitems = []

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

        return render(request, 'microsite/productapp.html', {'title':papp._get_tab_name(), 'rows':rows, 'pclass':pclass, 'pclasses':pclasses})

def weibo(request, item_id):
    weibopage = get_object_or_404(WeiboPage, pk=item_id)
    form = WeiboPageForm(request.POST, request.FILES, instance=weibopage)
    if not form.is_valid():
        return deal_with_errors(form)        
    else:
        weibopage = form.save(commit=False)
        return redirect(weibopage.url)

def link(request, item_id):
    linkpage = get_object_or_404(LinkPage, pk=item_id)
    form = LinkPageForm(request.POST, request.FILES, instance=linkpage)
    if not form.is_valid():
        return deal_with_errors(form)        
    else:
        linkpage = form.save(commit=False)
        return redirect(linkpage.url)


def content(request, item_id):
    content_page = get_object_or_404(ContentPage, pk=item_id)
    form = ContentPage(request.POST, request.FILES, instance=content_page)
    if not form.is_valid():
        return deal_with_errors(form)        
    else:
        content_page = form.save(commit=False)
        return render(request, 'microsite/contentpage.html', {'title':content_page.title, 'content':content_page.content})

def trend_item(request):
    form = TrendItemForm(request.POST, request.FILES, instance=None)
    if not form.is_valid():
        return deal_with_errors(form)        
    else:
        trenditem = form.save(commit=False)
        return render(request, 'microsite/contentpage.html', {'title':trenditem.title, 'content':trenditem.content.encode("utf8")})

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
        pics = []
        if caseitem.case_pic1:
            pics.append(caseitem.case_pic1)
        if caseitem.case_pic2:
            pics.append(caseitem.case_pic2)
        if caseitem.case_pic3:
            pics.append(caseitem.case_pic3)
        if caseitem.case_pic4:
            pics.append(caseitem.case_pic4)

        logger.debug("pics %s" % str(pics))
        logger.debug("pic1 %s" % caseitem.case_pic1)

        return render(request, 'microsite/item.html', {'title':caseitem.title, 'pics':pics, 'intro':caseitem.case_intro})

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
        pics = []
        if pitem.product_pic1:
            pics.append(pitem.product_pic1)
        if pitem.product_pic2:
            pics.append(pitem.product_pic2)
        if pitem.product_pic3:
            pics.append(pitem.product_pic3)
        if pitem.product_pic4:
            pics.append(pitem.product_pic4)

        logger.debug("pics %s" % str(pics))

        return render(request, 'microsite/item.html', {'title':pitem.title, 'pics':pics, 'intro':pitem.product_intro})


