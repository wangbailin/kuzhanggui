# coding: utf8
import logging, traceback
import re

from django.contrib.contenttypes.models import ContentType
from router import Router
from message_builder import MessageBuilder, BuildConfig
from framework.models import WXAccount
from microsite.models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rocket import settings
from microsite import consts

logger = logging.getLogger('weixin')
siteurl = 'http://jianfei.bestgames7.com'

def subscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s subscribe" % info.user)

def unsubscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s unsubscribe" % info.user)

def check_bind_state(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)

        if not wx_account.account.has_wx_bound:
            wx_account.state = WXAccount.STATE_BOUND
            wx_account.bind_time = datetime.now()
            wx_account.wxid = info.sp
            wx_account.save()

            wx_account.account.has_wx_bound = True
            wx_account.account.save()

            add_default_site(wx_account)

        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'绑定成功')
    except ObjectDoesNotExist:
        return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u'no wx account')

def match_subscribe_event(rule, info):
    return info.type == "event" and info.event == 'subscribe'

def match_unsubscribe_event(rule, info):
    return info.type == "event" and info.event == 'unsubscribe'

def match_location(rule, info):
    return info.type == 'location'

def match_menu(rule, info):
    return info.type == 'event' and re.match(r'menu_\d+', info.event_key) is not None

def match_submenu(rule, info):
    return info.type == 'event' and re.match(r'submenu_\d+_\d+', info.event_key) is not None

def micro_site(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        homepage = HomePage.objects.get(wx=wx_account)
        data = {}
        data['title'] = wx_account.name
        if homepage.message_description:
            data['description'] = homepage.message_description
        else:
            data['description'] = consts.DEFAULT_HOMEPAGE_MSG % wx_account.name
        if homepage.message_cover:
            data['pic_url'] = siteurl + homepage.message_cover.url
        data['url'] = siteurl + '/microsite/homepage/%d' % int(homepage.pk)
        return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

def find_nearest(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        contact_app = ContactApp.objects.get(wx=wx_account)
        contact_items = ContactItem.objects.filter(contact=contact_app)
        lat = float(info.lat)
        lng = float(info.lng)
        length = -1
        nearest = None
        for item in contact_items:
            cur_length = (item.lat - lat)**2 + (item.lng - lng)**2
            if length < 0 or cur_length < length:
                length = cur_length
                nearest = item
        if nearest is not None:
            logger.debug('start addr %f %f end addr %f %f' % (lat, lng, nearest.lat, nearest.lng))
            data = {}
            data['title'] = u'找到我们'
            data['description'] = u'点击查看如何找到我们。'
            data['pic_url'] = siteurl + settings.STATIC_URL + 'img/findme_message.png'
            data['url'] = siteurl + '/microsite/contact_map/%d/%f/%f' % (nearest.pk, lat, lng)
            return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
        else:
            return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'不知道怎么找到我们。')
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

def telephone(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        contact_app = ContactApp.objects.get(wx=wx_account)
        data = {}
        data['title'] = u'联系电话'
        data['description'] = u'点击查看我们的联系电话。'
        data['pic_url'] = siteurl + settings.STATIC_URL + 'img/kefuphone_message.png'
        data['url'] = siteurl + "/microsite/telephone/%d" % contact_app.pk
        return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

   

def trend(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        trend_app = TrendsApp.objects.get(wx=wx_account)
        data = {}
        data['title'] = trend_app.title
        if trend_app.message_description:
            data['description'] = message_description
        else:
            data['description'] = u'点击查看公司动态.'

        if trend_app.message_cover:
            data['pic_url'] = siteurl + settings.STATIC_URL + trend_app.message_cover.url
        else:
            data['pic_url'] = siteurl + settings.STATIC_URL + consts.DEFAULT_NEWS_COVER
        data['url'] = siteurl + "/microsite/trend/%d" % trend_app.pk
        return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

def join(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        joinpage = JoinPage.objects.get(wx=wx_account)
        data = {}
        data['title'] = joinpage.title
        if joinpage.message_description:
            data['description'] = joinpage.message_description
        else:
            data['description'] = u'点击查看最新招聘信息。'
        if joinpage.message_cover:
            data['pic_url'] = siteurl + settings.STATIC_URL + joinpage.message_cover.url
        else:
            data['pic_url'] = siteurl + settings.STATIC_URL + consts.DEFAULT_JOIN_COVER
        data['url'] = siteurl + "/microsite/join/%d" % joinpage.pk
        return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

def menu(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        match = re.match(r'menu_(\d+)', info.event_key)
        menu_id = match.group(1)

        menu = Menu.objects.get(id=menu_id)

        data = {}
        data['title'] = menu.name
        if menu.page.message_description:
            data['description'] = menu.page.message_description
        else:
            data['description'] = get_default_msg(menu.page)

        if menu.page.message_cover:
            data['pic_url'] = siteurl + menu.page.message_cover.url
        else:
            data['pic_url'] = siteurl + settings.STATIC_URL + get_default_cover(menu.page)

        data['url'] = siteurl + get_page_url(menu.page)
        return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

def submenu(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        match = re.match(r'submenu_(\d+)_(\d+)', info.event_key)
        menu_id = match.group(1)
        cls_id = match.group(2)

        menu = Menu.objects.get(id=menu_id)
        cls = None
        if menu.page.real_type == ContentType.objects.get_for_model(ProductApp):
            cls = ProductClass.objects.get(id=cls_id)
        elif menu.page.real_type == ContentType.objects.get_for_model(CaseApp):
            cls = CaseClass.objects.get(id=cls_id)

        if cls is not None:
            data = {}
            data['title'] = '%s - %s' % (menu.page.tab_name, cls.name)
            if menu.page.message_description:
                data['description'] = menu.page.message_description
            else:
                data['description'] = get_default_msg(menu.page)
            
            if menu.page.message_cover:
                data['pic_url'] = siteurl + menu.page.message_cover.url
            else:
                data['pic_url'] = siteurl + settings.STATIC_URL + get_default_cover(menu.page)
            data['url'] = siteurl + cls.get_url()
            return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
        else:
            return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

Router.get_instance().set({
        'name' : u'关注',
        'pattern' : match_subscribe_event,
        'handler' : micro_site 
    })
Router.get_instance().set({
        'name' : u'取消关注',
        'pattern' : match_unsubscribe_event,
        'handler' : unsubscribe
    })
Router.get_instance().set({
        'name' : u'验证绑定',
        'pattern' : u'rocket',
        'handler' : check_bind_state
    })
Router.get_instance().set({
        'name' : u'microsite',
        'pattern' : u'(官网|网站|你好|hi|hello|你是谁)',
        'handler' : micro_site,
    })
Router.get_instance().set({
        'name' : u'microsite',
        'pattern' : u'(动态|公司动态|新闻|公司新闻)',
        'handler' : trend,
    })
Router.get_instance().set({
        'name' : u'microsite',
        'pattern' : u'(招聘|职位|工作)',
        'handler' : join,
    })
Router.get_instance().set({
        'name' : u'location',
        'pattern' : match_location,
        'handler' : find_nearest,
    })

Router.get_instance().set({
        'name' : u'contact',
        'pattern' : u'电话',
        'handler' : telephone,
    })
Router.get_instance().set({
        'name' : u'menu',
        'pattern' : match_menu,
        'handler' : menu
    })

Router.get_instance().set({
        'name' : u'submenu',
        'pattern' : match_submenu,
        'handler' : submenu
    })
