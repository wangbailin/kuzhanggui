# coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig
from framework.models import WXAccount
from microsite.models import add_default_site
from datetime import datetime

def subscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s subscribe" % info.user)

def unsubscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s unsubscribe" % info.user)

def check_bind_state(rule, info):
    try:
        wx_account = WXAccount.objects.get(id=info.wx)

        if not wx_account.has_wx_bound:
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