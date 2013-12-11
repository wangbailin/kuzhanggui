# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import logging

from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from models import WallUser, WallMsg, WallItem
import datetime
from forms import WallItemForm
from framework.models import Account, WXAccount

logger = logging.getLogger('wall')

def _finish_all_msgs(item_id):#当活动结束的时候，有还没有上墙的消息的话全部改为已上墙状态
    wallmsgs = WallMsg.objects.filter(wall_item_id=item_id, flag_on=0)
    for wallmsg in wallmsgs:
        wallmsg.flag_on = 2
        wallmsg.flag_show = 3
        wallmsg.save()

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
@dajaxice_register
def add_wall_item(request, form):
    dajax = Dajax()
    form = WallItemForm(deserialize_form(form))
    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    
    if form.is_valid():
        wallItems =  WallItem.objects.filter(wx=wx_account)
        if (form.cleaned_data.get('id')):#change
            id = int(form.cleaned_data.get('id'))
            if not len(wallItems) == 0:
                for wallItem in wallItems:
                    if form.cleaned_data.get('keyword')==wallItem.keyword and not id==wallItem.id:
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '关键字不能重复！' }, 'addWallItemCallback')
                        return dajax.json()
                    if form.cleaned_data.get('begin_time')>=form.cleaned_data.get('end_time'):
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '结束时间不能小于开始时间！' }, 'addWallItemCallback')
                        return dajax.json()
                    if len(form.cleaned_data.get('event_name'))>20:
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '活动名称字数限制在20字以内！' }, 'addWallItemCallback')
                        return dajax.json()
                    if len(form.cleaned_data.get('keyword'))>20:
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '关键字字数限制在20字以内！' }, 'addWallItemCallback')
                        return dajax.json()
            flag_status=''
            if datetime.datetime.now()<form.cleaned_data.get('begin_time'):
                flag_status='未开始'
            elif datetime.datetime.now()>form.cleaned_data.get('end_time'):
                flag_status='已结束'
            else:
                flag_status='进行中'

            wallitem = WallItem.objects.get(pk=id)
            wallitem.event_name = form.cleaned_data.get('event_name').replace('\'','‘')
            wallitem.keyword = form.cleaned_data.get('keyword').replace('\'','‘')
            wallitem.begin_time=form.cleaned_data.get('begin_time')
            wallitem.end_time=form.cleaned_data.get('end_time')
            wallitem.welcome=form.cleaned_data.get('welcome').replace('\'','‘')
            wallitem.flag_check=form.cleaned_data.get('flag_check')
            wallitem.flag_status=flag_status
            wallitem.anonymity=form.cleaned_data.get('anonymity')
            wallitem.save()
            dajax.remove_css_class('#add_wall_item_form .control-group', 'error')
            dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'活动修改成功！' }, 'addWallItemCallback')
        else:#add
            if not len(wallItems) == 0:
                for wallItem in wallItems:
                    if form.cleaned_data.get('keyword')==wallItem.keyword:
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '关键字不能重复！' }, 'addWallItemCallback')
                        return dajax.json()
                    if form.cleaned_data.get('begin_time')>=form.cleaned_data.get('end_time'):
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '结束时间不能小于开始时间！' }, 'addWallItemCallback')
                        return dajax.json()
                    if len(form.cleaned_data.get('event_name'))>20:
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '活动名称字数限制在20字以内！' }, 'addWallItemCallback')
                        return dajax.json()
                    if len(form.cleaned_data.get('keyword'))>20:
                        dajax.add_data({ 'ret_code' : 100, 'ret_msg' : '关键字字数限制在20字以内！' }, 'addWallItemCallback')
                        return dajax.json()
            flag_status=''
            if datetime.datetime.now()<form.cleaned_data.get('begin_time'):
                flag_status='未开始'
            elif datetime.datetime.now()>form.cleaned_data.get('end_time'):
                flag_status='已结束'
            else:
                flag_status='进行中'
            wallitem = WallItem.objects.create(wx=wx_account, event_name=form.cleaned_data.get('event_name').replace('\'','‘'), keyword=form.cleaned_data.get('keyword').replace('\'','‘'), begin_time=form.cleaned_data.get('begin_time'), end_time=form.cleaned_data.get('end_time'), welcome=form.cleaned_data.get('welcome').replace('\'','‘'), flag_check=form.cleaned_data.get('flag_check'), flag_status=flag_status,  anonymity=form.cleaned_data.get('anonymity'))
            dajax.remove_css_class('#add_wall_item_form .control-group', 'error')
            dajax.add_data({ 'ret_code' : 0, 'ret_msg' : u'活动添加成功！' }, 'addWallItemCallback')
    else:
        dajax.remove_css_class('#add_wall_item_form .control-group', 'error')
        for error in form.errors:
            dajax.add_css_class('#%s' % error, 'error')
        dajax.add_data({ 'ret_code' : 1000, 'ret_msg' : '操作失败！' }, 'addWallItemCallback')
    return dajax.json()

@dajaxice_register
def get_new_messages_num(request, item_id):
    dajax = Dajax()
    wallitems = WallItem.objects.filter(pk=item_id)
    if not len(wallitems) == 0:#表示活动在
        wallitem = wallitems[0]
        now =datetime.datetime.now()
        flag_status = wallitem.flag_status
        if now < wallitem.begin_time:
            logger.info('活动还没有开始')
        elif now > wallitem.end_time:
            if flag_status == '进行中':
                wallitem.flag_status = '已结束' 
                finish_all_msgs(item_id)
                dajax.script("wall_item_tip()")
            else:
                logger.info('活动已结束')
        else:
            wallmsgs = WallMsg.objects.filter(flag_pass=0, flag_show=0, wall_item_id=item_id)
            new_messages_num = len(wallmsgs)
            if not new_messages_num == 0:
                dajax.assign('#newMsgNum','innerHTML',new_messages_num)
                dajax.add_data({'num':new_messages_num, 'event_name':wallitem.event_name} ,'changeTitle')
                dajax.remove_css_class('#new-message-num', 'noNews')
    else:
        dajax.script('itemDeleted()')
    return dajax.json()

@dajaxice_register
def get_new_messages(request, item_id):
    dajax = Dajax()
    wallitems = WallItem.objects.filter(id=item_id)
    if not len(wallitems) == 0:#活动存在
        wallitem = wallitems[0]
        if wallitem.flag_check == u"是":#需要审核
            wallmsgs = WallMsg.objects.filter(flag_pass=0, flag_show=0, wall_item_id=item_id)
            datas = []
            if not len(wallmsgs)==0:
                for wallmsg in wallmsgs:
                    logger.info('ddddd')
                    data = _get_data(wallitem.anonymity, wallmsg)
                    logger.info(data)
                    datas.append(data)
                    wallmsg.flag_show=1#说明已经上墙
                    wallmsg.save()
                dajax.add_data(datas, 'showNewMessages')
                dajax.add_css_class('div #new-message-num', 'noNews')
    return dajax.json()

@dajaxice_register
def pass_message(request, data_id):
    dajax = Dajax()
    wallmsg = WallMsg.objects.get(pk=data_id)
    wallitem = WallItem.objects.get(pk=wallmsg.wall_item_id)
    logger.info(wallitem)
    if wallmsg.flag_pass == 2:
        dajax.script('minus_len_reject()')
    data = _get_data(wallitem.anonymity, wallmsg)
    #create_time = wallmsg.create_time.strftime('%Y-%m-%d %H:%M')
    #pass_time = wallmsg.pass_time.strftime('%Y-%m-%d %H:%M') 
    #data = [wallmsg.type, wallmsg.content, wallmsg.user.nickname, wallmsg.pk, wallmsg.user.pic, create_time, pass_time]
    wallmsg.flag_pass=1#pass
    pass_time = datetime.datetime.now()
    wallmsg.pass_time = pass_time
    wallmsg.save()
    dajax.remove('div[data-id=%s]' % data_id)
    dajax.add_data(data,'showPassMessages')
    dajax.script('add_len_pass()')
    return dajax.json()

@dajaxice_register
def reject_message(request, data_id):
    dajax = Dajax()
    wallmsg = WallMsg.objects.get(pk=data_id)
    wallitem = WallItem.objects.get(pk = wallmsg.wall_item_id)
   # create_time = wallmsg.create_time.strftime('%Y-%m-%d %H:%M')
   # pass_time = wallmsg.pass_time.strftime('%Y-%m-%d %H:%M')
    data = _get_data(wallitem.anonymity, wallmsg)
   # data = [wallmsg.type, wallmsg.content, wallmsg.user.nickname, wallmsg.pk, wallmsg.user.pic, create_time, pass_time]
    wallmsg.flag_pass=2#reject
    reject_time = datetime.datetime.now()
    wallmsg.pass_time = reject_time#拒绝时间
    wallmsg.save()
    dajax.remove('div[data-id=%s]' % data_id)
    dajax.add_data(data,'showRejectMessages')
    dajax.script('add_len_reject()')
    return dajax.json()

@dajaxice_register#后台
def wall_message(request, data_id):
    dajax = Dajax()
    dajax.add_data(data_id, 'scroll')
    wallmsgs = WallMsg.objects.filter(pk=data_id)
    if not len(wallmsgs) == 0:
        for wallmsg in wallmsgs:
            if wallmsg.flag_on == 1:
                dajax.remove_css_class('div[data-id=%s]' % data_id, 'waiting')
                dajax.assign('div[data-id=%s] .state_wait' % data_id, 'innerHTML', '<span class="icon-white icon-ok flag"></span>已上墙')
                dajax.add_css_class('div[data-id=%s] .state_wait' % data_id, 'state')        
                dajax.remove_css_class('div[data-id=%s] .state_wait' % data_id, 'state_wait')
    return dajax.json()

@dajaxice_register#前台恢复以前数据
def message_on_wall_back(request, item_id):
    dajax = Dajax()
    datas = []
    wallitem = WallItem.objects.get(id=item_id)
    wallmsgs = WallMsg.objects.filter(flag_on=1, wall_item_id=item_id).order_by('-create_time')
    total = len(wallmsgs)
    if len(wallmsgs)==1:
        wallmsg = wallmsgs[0]
        data = _get_data(wallitem.anonymity, wallmsg)
        #nickname = str(wallmsg.user.nickname)
       # pic = str(wallmsg.user.pic)
       # data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic]
        datas.append(data)
    elif len(wallmsgs) ==2:
        wallmsg = wallmsgs[0]
        data = _get_data(wallitem.anonymity, wallmsg)
       # nickname = str(wallmsg.user.nickname)
       # pic = str(wallmsg.user.pic)
       # data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic]
        datas.append(data)
        wallmsg = wallmsgs[1]
        data = _get_data(wallitem.anonymity, wallmsg)
       # nickname = str(wallmsg.user.nickname)
       # pic = str(wallmsg.user.pic)
       # data = [wallmsg.type, wallmsg.content, nickname, wallmsg.pk, pic]
        datas.append(data)
    elif len(wallmsgs) >=3:
        wallmsg1 = wallmsgs[0]
        wallmsg2 = wallmsgs[1]
        wallmsg3 = wallmsgs[2]
        data1 = _get_data(wallitem.anonymity, wallmsg1)
        #nickname = str(wallmsg1.user.nickname)
        #pic = str(wallmsg1.user.pic)
        #data1 = [wallmsg1.type, wallmsg1.content, nickname, wallmsg1.pk, pic]
        data2 = _get_data(wallitem.anonymity, wallmsg2)
        #nickname = str(wallmsg2.user.nickname)
        #pic = str(wallmsg2.user.pic)
        #data2 = [wallmsg2.type, wallmsg2.content, nickname, wallmsg2.pk, pic]
        data3 = _get_data(wallitem.anonymity, wallmsg3)
        #nickname = str(wallmsg3.user.nickname)
        #pic = str(wallmsg3.user.pic)
        #data3 = [wallmsg3.type, wallmsg3.content, nickname, wallmsg3.pk, pic]
        if wallmsg1.type == 'image' and wallmsg2.type == 'text':
            datas.append(data2)
            datas.append(data1)
        if wallmsg1.type == 'image' and wallmsg2.type == 'image':
            datas.append(data1)
        if wallmsg1.type == 'text' and wallmsg2.type == 'image':
            datas.append(data2)
            datas.append(data1)
        if wallmsg1.type == 'text' and wallmsg2.type == 'text':
            if wallmsg3.type == 'text':
                datas.append(data3)
                datas.append(data2)
                datas.append(data1)
            else:
                datas.append(data2)
                datas.append(data1)
    else:
        datas = [] 
    logger.info(len(datas))
    for data in datas:
        dajax.add_data(data, 'onWall')
        dajax.assign('div[id="total"]', 'innerHTML', total )
    return dajax.json()

@dajaxice_register#前台
def message_on_wall(request, item_id, total):
    dajax = Dajax()
    data = []
    wallitems = WallItem.objects.filter(id=item_id)
    if not len(wallitems) == 0:
        wallitem = wallitems[0]
        now = datetime.datetime.now()
        flag_status = wallitem.flag_status
        if now > wallitem.end_time and flag_status == '进行中':#表示活动结束了
            wallitem.flag_status == '已结束'
            wallitem.save()
            finish_all_msgs(item_id) 
        if wallitem.flag_check == u"是":#need check
            wallmsgs = WallMsg.objects.filter(flag_pass=1, flag_on=0, wall_item_id=item_id).order_by('pass_time')
            if not len(wallmsgs) == 0:
                wallmsg = wallmsgs[0]
                wallmsg.flag_on = 1
                wallmsg.save()
                data = _get_data(wallitem.anonymity, wallmsg)
                #data = [wallmsg.type, wallmsg.content, wallmsg.user.nickname, wallmsg.pk, wallmsg.user.pic]
                dajax.add_data(data, 'onWall')
                total = int(total) + 1
                dajax.assign('div[id="total"]', 'innerHTML', total )
        else:#don't need check
            wallmsgs = WallMsg.objects.filter(flag_on=0, wall_item_id=item_id).order_by('create_time')
            if not len(wallmsgs) == 0:
                wallmsg = wallmsgs[0]
                wallmsg.flag_on = 1
                wallmsg.flag_pass = 1
                wallmsg.pass_time = datetime.datetime.now()
                wallmsg.save()
                data = _get_data(wallitem.anonymity, wallmsg)
                #data = [wallmsg.type, wallmsg.content, wallmsg.user.nickname, wallmsg.pk, wallmsg.user.pic]
                dajax.add_data(data, 'onWall')
                total = int(total) + 1
                dajax.assign('div[id="total"]', 'innerHTML', total )
        if  wallitem.end_time < datetime.datetime.now():
            dajax.script('refreshPage()')
    else:#活动已被删除
         dajax.script('itemDeleted()')
    return dajax.json()

@dajaxice_register
def refresh_flag_status(request):#刷新活动的状态
    dajax = Dajax()
    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    
    now = datetime.datetime.now()
    wallitems = WallItem.objects.filter(wx=wx_account)
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
    return dajax.json() 
            
@dajaxice_register
def delete_wall_item(request, item_id):
    dajax = Dajax()
    wallitems = WallItem.objects.filter(id=item_id)
    if len(wallitems) == 0:
        dajax.script('itemDeleted()') 
    return dajax.json()

@dajaxice_register
def get_state(request, item_id):
    dajax = Dajax()
    wallitems = WallItem.objects.filter(id=item_id)
    now = datetime.datetime.now()
    if not len(wallitems) == 0:
        wallitem = wallitems[0]
        if wallitem.begin_time <= now:#表示开始
            dajax.script('refreshPage()')
    return dajax.json()
