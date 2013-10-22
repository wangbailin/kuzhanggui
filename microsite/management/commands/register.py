#coding: utf-8

import sys, struct, os, logging, traceback, heapq, datetime

from django.core.management import setup_environ
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from framework.models import Account, WXAccount 
from microsite.models import *
from microsite.models import add_default_site

class Command(BaseCommand):
    args = '<username password>'

    PHONE = '18640287525'
    QQ = '491320274'
    EMAIL = 'test@jiaoyin.cm'
    PASSWORD = 'nameLR9969'

    def handle(self, *args, **options):
        if len(args) <= 0:
            print Command.args
            return

        username = args[0]
        password = Command.PASSWORD if len(args) == 1 else args[1] 

        new_user = User.objects.create_user(username = username,
            password = password,
            email = Command.EMAIL)
        new_account = Account.objects.create(user=new_user, 
            phone= Command.PHONE,
            qq = Command.QQ,
            expired_time=datetime.datetime.now() + datetime.timedelta(weeks=8))
        new_account.user.groups = Group.objects.filter(name=u'试用账户')

