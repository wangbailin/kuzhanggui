# coding: utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.utils.encoding import smart_str, smart_unicode
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import logging, traceback, time, struct, socket
import hashlib
from datetime import date, timedelta, datetime

import rules
from pyweixin import WeiXin
from router import Router
from message_builder import MessageBuilder, BuildConfig

from framework.models import WXAccount

router_error = None
router_reply = None
def _route_callback(error=None, reply=None):
    global router_error, router_reply
    router_error = error
    router_reply = reply

@csrf_exempt
def index(request, wx):
    global router_error, router_reply
    wxlogger = logging.getLogger('weixin')
    
    if request.method == 'GET':
        if 'signature' not in request.GET or 'timestamp' not in request.GET or 'nonce' not in request.GET or 'echostr' not in request.GET:
                return HttpResponse('bad request %s' % str(request.GET))
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        wxlogger.info("receive one get message signature %s timestamp %s nonce %s echostr %s" % (signature, timestamp, nonce, echostr))
	token = cache.get('wx_%s_token' % wx)
        weixin = WeiXin.on_connect(token, timestamp, nonce, signature, echostr)
        if weixin.validate():
            return HttpResponse(echostr, content_type="text/plain")
        else:
            return HttpResponse(None, content_type="text/plain")
    elif request.method == 'POST':
        try:
            weixin = WeiXin.on_message(smart_str(request.raw_post_data))
            message = weixin.to_json()
            wxlogger.info("receive one message %s" % str(message))

            Router.get_instance().reply(wx, message, _route_callback)
            
            if router_error is None and router_reply is not None:
                router_reply.platform = MessageBuilder.PLATFORM_WEIXIN
                if router_reply.type != MessageBuilder.TYPE_NO_RESPONSE:
                    wxlogger.info("reply success type %s platform %s data %s" % (router_reply.type, router_reply.platform, router_reply.data))
                    return HttpResponse(MessageBuilder.build(message, router_reply), content_type="application/xml")
                else:
                    wxlogger.info("%s", router_reply.data)
            else:
                wxlogger.info("router error %s router reply %s" % (str(router_error), str(router_reply)))
                return HttpResponse('<xml></xml>', content_type="application/xml")
        except:
            wxlogger.error(traceback.format_exc())
            reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, u"抱歉，我不是很明白。")
            return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
