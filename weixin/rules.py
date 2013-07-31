# coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig

def subscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s subscribe" % info.user)

def unsubscribe(rule, info):
    return BuildConfig(MessageBuilder.TYPE_NO_RESPONSE, None, u"%s unsubscribe" % info.user)

def check_bind_state(rule, info):
    pass

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