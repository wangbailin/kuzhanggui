import os
#substitute mysite with the name of your project !!!
os.environ['DJANGO_SETTINGS_MODULE'] = 'rocket.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
