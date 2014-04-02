#coding: utf-8

import os.path
import shutil

from datetime import datetime

from django.core.management.base import BaseCommand 
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        def copy(dir):
            src =  "./resources/" + dir
            target = settings.MEDIA_ROOT + dir

            if os.path.isdir(target):
                shutil.rmtree(target)

            shutil.copytree(src, target)

        for dir in ["img", "themes"]:
            copy(dir)
        print "done"
