#!/usr/local/bin/python2.7
#coding: utf-8

import sys, struct, os, logging, traceback, heapq
sys.path.append("..")

from datetime import datetime

from django.core.management import setup_environ
from django.utils.timezone import utc

from rocket import settings

setup_environ(settings)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from framework.models import Account, WXAccount 
from microsite.models import *
from microsite.models import add_default_site

if __name__ == '__main__':
    wx = WXAccount.objects.filter(pk=25)
    if len(wx) == 0:
        wx = WXAccount()
        wx.account = account
        wx.name = username
        wx.follower_count = 0
        wx.message_count = 0
        wx.username = username
        wx.state = 4
        wx.url = 'abc'
        wx.token = 'abc'
        wx.bind_time = datetime.utcnow().replace(tzinfo=utc)
        wx.save()
    else:
        wx = wx[0]
        print "aleady one weixin account"

    add_default_site(wx)

    
