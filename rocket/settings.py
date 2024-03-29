# Django settings for rocket project.
import os

DEBUG = False
#DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'rocket',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'nameLR9969',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['jianfei.bestgames7.com','r.limijiaoyin.com', 
		'wangnan.limijiaoyin.com', 'yangchen.limijiaoyin.com', 'kuzhanggui.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_CN'
FILE_CHARSET='UTF-8'
DEFAULT_CHARSET = 'UTF-8'
#DEFAULT_FILE_STORAGE = 'baidu_yun.storage.BaiduYunStorage'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(os.path.normpath(__file__))))
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/data/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
#MEDIA_URL = 'http://r.limijiaoyin.com/media/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/opt/rocket/templates/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_ROOT + '/templates',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
SITE_URL = "http://www.kuzhanggui.com"

CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_UPLOAD_PATH = '/data/media/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-'],        
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],        
            ['Bold','Italic','Underline','Strike','-'],        
            ['NumberedList','BulletedList','-','Blockquote'],        
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],        
            ['Link','Unlink'],        
            ['Image','Flash','HorizontalRule','Smiley','SpecialChar','TextColor','BGColor'],        
            ['Styles','Format','Font','FontSize'],        
            ['Maximize','ShowBlocks','Preview','Source'],
        ],
        'language': 'zh-cn',
        'width': 760,
        'height': 300,
        'image_previewText': 'image',
        'toolbarCanCollapse': False,
    },
    'awesome_ckeditor': {
        'toolbar': 'Basic',
    },
}

AUTO_RENDER_SELECT2_STATICS = False

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder'
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p+o0k1+5u#84x^pe(b($zp@m(5b501o2$(j*(+v-_)9&4jp1vq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages")


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'framework.middlewares.CsrfFixMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
	'django_user_agents.middleware.UserAgentMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_URL = '/welcome'

ROOT_URLCONF = 'rocket.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rocket.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django_user_agents',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'framework',
    'microsite',
    'data',
    'wall',
    'ajax_upload',
    'django_tables2',
    'django_select2',
    'dajaxice',
    'dajax',
    'chartit',
    'ckeditor',
    'cronjobs',
    'baidu_yun',
    'datetimewidget',
   # 'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT + '/logs/','rocket_default.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'wall': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT + '/logs/','wall.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'weixin': {
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT + '/logs/','weixin.log'),
            'when':'midnight',
            'backupCount': 0,
            'formatter':'standard',
        },
        'sts': {
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT + '/logs/','sts.log'),
            'when':'midnight',
            'backupCount': 0,
            'formatter':'standard',
        },
        'django': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT + '/logs/','django.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'default': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'cron': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'wall': {
            'handlers': ['wall'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'pyhttpclient': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'weixin': {
            'handlers': ['weixin'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sts': {
            'handlers': ['sts'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['django'],
            'level': DEBUG,
            'propagate': False

        }
    }
}
