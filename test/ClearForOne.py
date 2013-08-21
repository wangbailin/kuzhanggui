#!/usr/local/bin/python2.7
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
if __name__ == '__main__':
    wx_account = WXAccount(pk=23)
    HomePage.objects.filter(wx=wx_account).delete()
    IntroPage.objects.filter(wx=wx_account).delete()
    CulturePage.objects.filter(wx=wx_account).delete()
    JoinPage.objects.filter(wx=wx_account).delete()
    WeiboPage.objects.filter(wx=wx_account).delete()

    TrendsApp.objects.filter(wx=wx_account).delete()
    ContactApp.objects.filter(wx=wx_account).delete()
    CaseApp.objects.filter(wx=wx_account).delete()
    ProductApp.objects.filter(wx=wx_account).delete()


