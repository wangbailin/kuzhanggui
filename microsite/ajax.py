# -*- coding: utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from django.core.cache import cache
from django.contrib.auth import authenticate, login
import random

from framework.models import Account, WXAccount
from microsite.models import Menu
from microsite.forms import AddEditMenuForm

@dajaxice_register
def add_edit_menu(request, form):
    dajax = Dajax()
    form = AddEditMenuForm(deserialize_form(form))

    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    if form.is_valid():
        menu = Menu(wx=wx_account, page=form.cleaned_data.get('page'), name=form.cleaned_data.get('name'))
        menu.save()
        dajax.remove_css_class('#edit_account_form .control-group', 'error')
        dajax.add_data({ 'ret_code' : 0, 'ret_msg' : 'success' }, 'addEditMenuCallback')
    else:
        dajax.remove_css_class('#edit_account_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : 'error' }, 'addEditMenuCallback')

    return dajax.json()