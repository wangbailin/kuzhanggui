#coding: utf-8

import os.path
import shutil

from datetime import datetime

from django.core.management.base import BaseCommand 
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        target = settings.MEDIA_ROOT + "themes"
        if os.path.isdir(target):
            shutil.rmtree(target)
        shutil.copytree("./themes", target)
        print "done"
        

