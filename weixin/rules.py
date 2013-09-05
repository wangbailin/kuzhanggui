# coding: utf8
import logging, traceback

from router import Router
from message_builder import MessageBuilder, BuildConfig
from framework.models import WXAccount
from microsite.models import *
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rocket import settings

logger = logging.getLogger('weixin')
#siteurl = 'http://r.limijiaoyin.com'
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


def micro_site(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        homepage = HomePage.objects.get(wx=wx_account)
        data = {}
        data['title'] = u'欢迎光临微官网'
        data['description'] = homepage.message_description
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
            data['title'] = u'导航位置'
            data['description'] = u'已为您搜索到最近的公司地址，查看位置并导航，请点击进入！'
            data['pic_url'] = siteurl + settings.STATIC_URL + 'img/findme_message.png'
            data['url'] = siteurl + '/microsite/contact_map/%d/%f/%f' % (nearest.pk, lat, lng)
            return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
        else:
            return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'没有找到公司')
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'非常抱歉')

def telephone(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        contact_app = ContactApp.objects.get(wx=wx_account)
        data = {}
        data['title'] = u'客服电话'
        data['description'] = u'欢迎联系我们，您查询的同时可以一键拨号，更多客服号码，请点击进入！'
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
        data['description'] = u'点击查看公司动态'
        data['pic_url'] = siteurl + settings.STATIC_URL + 'img/news_message.png'
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
        data['description'] = u'点击查看公司招聘信息'
        data['pic_url'] = siteurl + settings.STATIC_URL + 'img/joinus_message.png'
        data['url'] = siteurl + "/microsite/join/%d" % joinpage.pk
        return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
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
        'name' : u'location',
        'pattern' : u'电话',
        'handler' : telephone,
    })
