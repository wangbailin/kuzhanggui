#coding:utf8
from django.contrib.contenttypes.models import ContentType
from rocket import settings

DEFAULT_HOMEPAGE_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/homepage_message.png'
DEFAULT_INTRO_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/intro_message.png'
DEFAULT_BUSINESS_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/business_message.png'
DEFAULT_NEWS_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/news_message.png'
DEFAULT_PRODUCT_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/product_message.png'
DEFAULT_CASE_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/case_message.png'
DEFAULT_WEIBO_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/weibo_message.png'
DEFAULT_CONTACT_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/kefuphone_message.png'
DEFAULT_JOIN_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/joinus_message.png'
DEFAULT_HELP_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/help_message.png'
DEFAULT_CONTENT_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/content_message.png'
DEFAULT_LINK_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/link_message.png'
DEFAULT_FINDME_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/findme_message.png'
DEFAULT_TRENDITEM_COVER = settings.SITE_URL + settings.STATIC_URL + 'img/default_trenditem_cover.png'
DEFAULT_COVER = settings.SITE_URL + settings.STATIC_URL + "img/empty.png"

DEFAULT_HOMEPAGE_MSG = u'点击查看%s微官网。'
DEFAULT_INTRO_MSG = u'点击查看公司介绍。'
DEFAULT_BUSINESS_MSG = u'点击查看公司业务。'
DEFAULT_NEWS_MSG = u'点击查看公司动态。'
DEFAULT_CASE_MSG = u'点击查看公司案例。'
DEFAULT_PRODUCT_MSG = u'点击查看公司产品。'
DEFAULT_WEIBO_MSG = u'点击查看公司官方微博。'
DEFAULT_CONTACT_MSG = u'点击查看公司联系方式。'
DEFAULT_JOIN_MSG = u'点击查看公司最新招聘信息。'
DEFAULT_HELP_MSG = u'点击查看新手指导。'
DEFAULT_MSG = "点击查看全部内容。"

DEFAULT_INTRO_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_intro.png'
DEFAULT_BUSINESS_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_business.png'
DEFAULT_NEWS_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_news.png'
DEFAULT_PRODUCT_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_product.png'
DEFAULT_CASE_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_case.png'
DEFAULT_WEIBO_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_weibo.png'
DEFAULT_CONTACT_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_contact.png'
DEFAULT_JOIN_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_joinus.png'
DEFAULT_HELP_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/home_help.png'
DEFAULT_ICON = settings.SITE_URL + settings.STATIC_URL + 'themes/%s/default.png'
