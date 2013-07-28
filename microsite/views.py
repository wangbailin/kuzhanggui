# Create your views here.

import logging
from django.shortcuts import render_to_response, get_object_or_404, render, redirect

from forms import HomePageForm, IntroPageForm, FormManager

from django.contrib.auth import authenticate

from models import *
from account.models import *


def get_tabs(request):
    username = 'jfwang213'
    password = 'nameLR9969'
    user = authenticate(username=username, password=password)
    account = Account.objects.get(user=user)
    wx = Weixin.objects.get(account=account)
    pages = Page.objects.filter(wx=wx)
    tabs = []
    for p in pages:
        subp = p.cast()
        form = FormManager.get_form(subp)
        tabs.append( (subp, form) )
    return tabs


def setting(request, active_tab_id = None):
    if active_tab_id:
        active_tab_id = int(active_tab_id)
    else:
        active_tab_id = 1
    tabs = get_tabs(request)
    return render(request, "setting.html", {"tabs":tabs, "active_tab_id":active_tab_id})


def save(request, page_id):
    logger = logging.getLogger('default')
    if page_id:
        page_id = int(page_id)
        logger.debug("save page id %d" % page_id)
        page = get_object_or_404(Page, id = page_id)
        sub_page = page.cast()
        if page.real_type == ContentType.objects.get_for_model(HomePage):
            logger.debug("home page")
            form = HomePageForm(request.POST, request.FILES, instance=page.cast())
        elif page.real_type == ContentType.objects.get_for_model(IntroPage):
            logger.debug("intro page")
            form = IntroPageForm(request.POST, request.FILES, instance=page.cast())
        else:
            logger.error("bad real_type %d" % page.read_type.id)
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

