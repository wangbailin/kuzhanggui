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
import redis
from pyweixin import WeiXin
from router import Router
from message_builder import MessageBuilder, BuildConfig

from framework.models import WXAccount
from wall.models import WallUser, WallItem, WallMsg
from wall.utils import judge_symbol

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
    r = redis.StrictRedis(host='localhost', port=6379, db=0)    
 
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
            wx_account = WXAccount.objects.get(id=wx)
            wx_account.message_count += 1
            wx_account.save()
            wxlogger.info("receive one message %s" % str(message))
            

            if message['MsgType'] == 'event' and message['Event'] == 'subscribe':
                walluser, created = WallUser.objects.get_or_create(wx=wx_account, openid=message['FromUserName'])
                walluser.wall_item_id='0'
                walluser.save() 
                r.rpush('userList', message['FromUserName'])
                wxlogger.info("我要订阅")
            if message['MsgType'] == 'text' or message['MsgType'] == 'image' or message['MsgType'] == 'voice':
                wxlogger.info("我想上墙")
                wxlogger.info(len(WallUser.objects.filter(wx=wx_account, openid=message['FromUserName'])))
                if not len(WallUser.objects.filter(wx=wx_account, openid=message['FromUserName']))==0:
                    walluser = WallUser.objects.filter(wx=wx_account, openid=message['FromUserName'])[0]
                    #wxlogger.info('walluser is %s' % message['FromUserName'])
                    if not walluser.wall_item_id == '0':#说明上墙了
                        #对上墙活动的进行时间进行判断，有可能上墙了但活动已经结束了
                        wallitem = WallItem.objects.filter(id=walluser.wall_item_id)
                        if len(wallitem) == 0:
                            walluser.wall_item_id = '0'
                            walluser.save()
                            reply_str = "活动不存在"
                            reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, reply_str)
                            return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
                        else:
                            wallitem = wallitem[0]
                        #结束时间10分钟后的处理
                        #if (datetime.now()-wallitem.begin_time).seconds <= 600:
                        if datetime.now()<wallitem.end_time:#说明在上墙时间内
                            if message['MsgType'] == 'text' or message['MsgType'] == 'voice':
                                message_str = ""
                                if message['MsgType'] == 'text':
                                    message_str = message['Content']
                                else:
                                    message_str = message['Recognition']
                                if not message_str == "退出":
                                    wxlogger.info('receive message %s' % message_str)
                                    WallMsg.objects.create(user=walluser, type='text', content=message_str, wall_item_id=walluser.wall_item_id)
                                    reply_str = "发送成功"
                                    wxlogger.info(datetime.now())
                                    reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, reply_str)
                                    return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")

                                else:#quit the wall
                                    walluser.wall_item_id = '0'
                                    walluser.save()
                                    reply_str = "退出成功"
                                    reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, reply_str)
                                    return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
                            else:#image
                                WallMsg.objects.create(user=walluser, type=message['MsgType'], content=message['PicUrl'], wall_item_id=walluser.wall_item_id)
                                reply_str = "发送成功"
                                reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, reply_str)
                                return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
                        if (datetime.now()-wallitem.end_time).seconds <= 600:#超出上墙时间不到10分钟
                            reply_str = "活动已结束，您将在10分钟之后自动退出该活动，您也可以回复“退出”直接退出该活动。"
                            reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, reply_str)
                            return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
                        else:
                            walluser.wall_item_id = '0'
                            walluser.save()
                            wxlogger.info("活动已经结束超过10分钟，您已经被系统退出上墙。")
                            reply_str = "活动已经结束超过10分钟，您已经被系统退出上墙。"
                            reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, reply_str)
                            return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
                    else:#说明没有上墙
                        if message['MsgType'] == 'text':
                            wxlogger.info(message)
                            wxlogger.info("说明没有上墙")
                            if not len(WallItem.objects.filter(wx=wx_account)) == 0:#说明该微信号有微信墙活动
                                for wallitem in WallItem.objects.filter(wx=wx_account):
                                    if message['Content']==wallitem.keyword:#说明有上墙的关键字
                                        reply_str = ""
                                        if datetime.now()<wallitem.begin_time:#没有开始
                                            reply_str = "活动未开始，请在活动开始("+str(wallitem.begin_time)+")之后再发送消息。"
                                        elif datetime.now()>wallitem.end_time:#说明已经结束
                                            reply_str = "活动已结束"
                                        else:
                                            wxlogger.info(wallitem.welcome)
                                            walluser.wall_item_id = wallitem.id
                                            walluser.save()
                                            if judge_symbol(wallitem.welcome):
                                                reply_str = wallitem.welcome+'回复“退出”则退出上墙。'
                                            else:
                                                reply_str = wallitem.welcome+','+'回复“退出”则退出上墙。'
                                        reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, reply_str)
                                        return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
                                    
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
                reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, u"抱歉，我不是很明白")
                return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
                #return HttpResponse('<xml></xml>', content_type="application/xml")
        except:
            wxlogger.error(traceback.format_exc())
            reply_config = BuildConfig(MessageBuilder.TYPE_RAW_TEXT, MessageBuilder.PLATFORM_WEIXIN, u"抱歉，我不是很明白。")
            return HttpResponse(MessageBuilder.build(message, reply_config), content_type="application/xml")
