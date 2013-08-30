# coding: utf8
import logging, traceback

from router import Router
from message_builder import MessageBuilder, BuildConfig
from framework.models import WXAccount
from microsite.models import add_default_site, HomePage
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('weixin')
siteurl = 'http://r.limijiaoyin.com'

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


def micro_site(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)
        homepage = HomePage.objects.get(wx=wx_account)
        data = {}
        data['title'] = u'欢迎光临微官网'
        data['description'] = u'这个是描述'
        data['pic_url'] = siteurl + homepage.cover.url
        data['url'] = siteurl + '/microsite/homepage/%d' % int(homepage.pk)
        return BuildConfig(MessageBuilder.TYPE_WEB_APP, None, data)
    except:
        logger.error(traceback.format_exc())
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u'绑定成功')

Router.get_instance().set({
        'name' : u'关注',
        'pattern' : match_subscribe_event,
        'handler' : subscribe
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
        'pattern' : u'官网',
        'handler' : micro_site,
    })
