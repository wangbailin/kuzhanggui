import sys, struct, os, logging, traceback, heapq, datetime

from django.core.management import setup_environ
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc
           
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
                 
from framework.models import Account, WXAccount
from microsite.models import *
from microsite.models import add_default_site
import data.cron

#from django.core.management.base import BaseCommand,commandError

class Command(BaseCommand):
    def handle(self,*args,**options):
        data.cron.weixin_daily_analyse()
