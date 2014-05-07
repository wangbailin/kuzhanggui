# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render_to_response, get_object_or_404, render, redirect

from django.contrib import auth
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from datetime import datetime
import django_tables2 as tables
from models import WallItem, WallUser, WallMsg
from django.contrib.contenttypes.models import ContentType
from tables import WallTable
from forms import WallItemForm
from microsite.wx_match import *
from verify import *
logger = logging.getLogger('wall')
from utils import judge_os_br

def get_apps(request):
    account = Account.objects.get(user=request.user)
    wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    apps = App.objects.filter(wx=wx)
    return apps

def _get_data(anonymity, wallmsg):
    data = []
    logger.info(anonymity)
    if anonymity == '否':
        nickname = '匿名'
        pic = '/static/img/default_avatar.png'
        create_time = wallmsg.create_time.strftime('%Y-%m-%d %H:%M')
        pass_time = wallmsg.pass_time.strftime('%Y-%m-%d %H:%M')
        data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic, create_time, pass_time]
        logger.info(data)
    else:
        nickname = str(wallmsg.user.nickname)
        pic = str(wallmsg.user.pic)
        create_time = wallmsg.create_time.strftime('%Y-%m-%d %H:%M')
        pass_time = wallmsg.pass_time.strftime('%Y-%m-%d %H:%M')
        data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic, create_time, pass_time]
    logger.info(data)
    return data


@cal_time
@login_required
@bind_wx_check
def wall(request):
    if 'active_wx_id' in request.session:
        wx = get_object_or_404(WXAccount, pk=request.session['active_wx_id'])
    else:
        user = auth.get_user(request)
        account = Account.objects.get(user=user)

        wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
        request.session['active_wx_id'] = wx.pk
    
    wall_item_nums = []
    now = timezone.now()
    logger.info('now time is %s' % now)
    wallitems = WallItem.objects.filter(wx=wx)
    if not len(wallitems)==0:
        for wallitem in wallitems:
            if now < wallitem.begin_time:
                wallitem.flag_status = '未开始'
            if now > wallitem.end_time:
                if (now-wallitem.end_time).seconds > 600:
                    wallusers = WallUser.objects.filter(wall_item_id=wallitem.id)
                    if not len(wallusers) == 0:
                        for walluser in wallusers:
                            walluser.wall_item_id = '0'
                            walluser.save()
                wallitem.flag_status = '已结束'
            if now > wallitem.begin_time and now < wallitem.end_time:
                wallitem.flag_status = '进行中'
        wallitem.save()
        wall_item_nums.append(wallitem.pk)
    wall_info = WallTable(WallItem.objects.filter(wx=wx), prefix='wt-')
    wall_info.paginate(page=request.GET.get(wall_info.prefix+"page",1), per_page=10)
    form = WallItemForm()
    logger.info(wall_item_nums)
    return render(request, "wall.html",{'wall_info':wall_info, 'form':form, 'wall_item_nums':wall_item_nums, 'apps' : get_apps(request)})

@cal_time
@login_required
@bind_wx_check
@wall_item_verify('item_id')
def wall_delete(request, item_id):
    item = get_object_or_404(WallItem, pk = item_id)
    item.delete()
    wallusers = WallUser.objects.filter(wall_item_id=item_id)
    wallmsgs = WallMsg.objects.filter(wall_item_id=item_id)
    if not len(wallusers) == 0:
        for walluser in wallusers:
            walluser.wall_item_id = '0'
            walluser.save()
    if not len(wallusers) == 0:
        for wallmsg in wallmsgs:
            wallmsg.delete()
    return redirect('/weixinwall')

@cal_time
@login_required
@bind_wx_check
@wall_item_verify('item_id')
def wall_show(request, item_id):
    wallitem = get_object_or_404(WallItem, pk = item_id)
    wxaccount = wallitem.wx
    wxname = wxaccount.name
    logger.info(wxname)
    flag_status = wallitem.flag_status
    event_name = wallitem.event_name
    begin_time = wallitem.begin_time
    end_time = wallitem.end_time
    now = datetime.now()
    if now < begin_time:
        return render(request, 'wall_show_dns.html', {'wallitem':wallitem, 'weixinname':wxname})
    if now < end_time and now > begin_time:
        return render(request, 'wall_show.html',{'wallitem':wallitem, 'weixinname':wxname})
    if now > end_time:
        return render(request, 'wall_show_complete.html',{'name':event_name})

@cal_time
@login_required
@bind_wx_check
@wall_item_verify('item_id')
@wall_item_check('item_id')
def wall_conduct(request, item_id):#下面的信息均为已上墙过滴
    wallmsgs_new = WallMsg.objects.filter(flag_pass=0, flag_show=1, wall_item_id=item_id)
    event_name = WallItem.objects.get(id=item_id).event_name
    datas_new = []
    len_datas_pass = 0
    len_datas_reject = 0
    wallitem = WallItem.objects.get(pk=item_id)
    if not len(wallmsgs_new) == 0:
        for wallmsg in wallmsgs_new:
            data = _get_data(wallitem.anonymity, wallmsg)
            #nickname = str(wallmsg.user.nickname)
            #pic = str(wallmsg.user.pic)
            #data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic, wallmsg.create_time, wallmsg.pass_time]
            datas_new.append(data)
    #审核是否需要分两个，一个已上墙，一个未上墙
    wallmsgs_pass_on = WallMsg.objects.filter(flag_pass=1, flag_on=1, flag_show=1, wall_item_id=item_id).order_by('pass_time')
    datas_pass_on = []
    if not len(wallmsgs_pass_on) == 0:
        for wallmsg in wallmsgs_pass_on:
            data = _get_data(wallitem.anonymity, wallmsg)
            #nickname = str(wallmsg.user.nickname)
            #pic = str(wallmsg.user.pic)
            #data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic, wallmsg.create_time, wallmsg.pass_time]
            datas_pass_on.append(data)
    wallmsgs_pass_noton = WallMsg.objects.filter(flag_pass=1, flag_on=0, flag_show=1, wall_item_id=item_id).order_by('pass_time')
    datas_pass_noton = []
    if not len(wallmsgs_pass_noton) == 0:
        for wallmsg in wallmsgs_pass_noton:
            data = _get_data(wallitem.anonymity, wallmsg)
            #nickname = str(wallmsg.user.nickname)
            #pic = str(wallmsg.user.pic)
            #data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic, wallmsg.create_time, wallmsg.pass_time]
            datas_pass_noton.append(data)
    len_datas_pass = len(datas_pass_on) + len(datas_pass_noton)
    wallmsgs_reject = WallMsg.objects.filter(flag_pass=2, flag_show=1, wall_item_id=item_id).order_by('pass_time')
    datas_reject = []
    if not len(wallmsgs_reject) == 0:
        for wallmsg in wallmsgs_reject:
            data = _get_data(wallitem.anonymity, wallmsg)
            #nickname = str(wallmsg.user.nickname)
            #pic = str(wallmsg.user.pic)
            #data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic, wallmsg.create_time, wallmsg.pass_time]
            datas_reject.append(data)
    len_datas_reject = len(datas_reject)
    return render(request, 'wall_conduct.html', {'event_name':event_name, 'item_id':item_id, 'datas_new':datas_new, 'datas_pass_on':datas_pass_on, 'datas_pass_noton':datas_pass_noton, 'datas_reject':datas_reject, 'len_datas_pass':len_datas_pass, 'len_datas_reject': len_datas_reject})

