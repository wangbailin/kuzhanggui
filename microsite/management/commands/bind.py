#coding: utf-8

import sys, struct, os, logging, traceback, heapq

from datetime import datetime

from django.core.management import setup_environ
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from framework.models import Account, WXAccount 
from microsite.models import *
from microsite.models import add_default_site

class Command(BaseCommand):
    args = '<username>'

    def handle(self, *args, **options):
        if len(args) <= 0:
            print 'no username'
            return

        username = args[0]
        user = User.objects.filter(username=username)

        if len(user) == 0:
            print 'user not found'
            return

        accounts = Account.objects.filter(user=user[0])
        if len(accounts) <= 0:
            print 'account not found'
            return

        account = accounts[0]
        wxAccounts = WXAccount.objects.filter(account=account)
        if len(wxAccounts) > 0:
            result = raw_input("weixin account exists, rebind?(y no n):")
            if result != 'y' and result != 'Y':
                return

        wx = wxAccounts[0] if len(wxAccounts) > 0 else WXAccount()
        wx.account = account
        wx.name = username
        wx.follower_count = 0
        wx.message_count = 0
        wx.username = username
        wx.state = 4
        wx.url = 'abc'
        wx.token = 'abc'
        wx.bind_time = datetime.utcnow().replace(tzinfo=utc)
        wx.app_id = 'test'
        wx.wxid = username
        wx.app_secret = 'test, too'
        wx.save()
        add_default_site(wx)

        account.has_wx_bound = True
        account.save()
    
        print 'OK!'

