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
        if len(args) < 1:
            print Command.args
            return

        user = User.objects.get(username=args[0])
        account = Account.objects.get(user=user)
        wx = WXAccount.objects.get(account=account)
        pages = Page.objects.filter(wx=wx)

        count = 11
        for page in pages:
            subp = page.cast()
            subp.enable = True
            if subp.real_type == ContentType.objects.get_for_model(HomePage):
                subp.setPosition(0)
            elif subp.real_type == ContentType.objects.get_for_model(IntroPage):
                subp.setPosition(1)
            elif subp.real_type == ContentType.objects.get_for_model(BusinessPage):
                subp.setPosition(2)
            elif subp.real_type == ContentType.objects.get_for_model(TrendsApp):
                subp.setPosition(3)
            elif subp.real_type == ContentType.objects.get_for_model(TeamApp):
                subp.setPosition(4)
            elif subp.real_type == ContentType.objects.get_for_model(ProductApp):
                subp.setPosition(5)
            elif subp.real_type == ContentType.objects.get_for_model(CaseApp):
                subp.setPosition(6)
            elif subp.real_type == ContentType.objects.get_for_model(WeiboPage):
                subp.setPosition(7)
            elif subp.real_type == ContentType.objects.get_for_model(ContactApp):
                subp.setPosition(8)
            elif subp.real_type == ContentType.objects.get_for_model(JoinPage):
                subp.setPosition(9)
            elif subp.real_type == ContentType.objects.get_for_model(HelpPage):
                subp.setPosition(10)
            else:
                subp.setPosition(count)
                subp.enable = False
                count += 1

            subp.save()

