#coding:utf8
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from rocket import settings
from framework.models import WXAccount

class WallItem(models.Model):
    wx = models.ForeignKey(WXAccount, verbose_name = u'微信账号')
    event_name = models.CharField(u'活动名称', max_length=100)
    keyword = models.CharField(u'关键字', max_length=100)
    pub_time = models.DateTimeField(u'日期', auto_now_add=True)
    welcome = models.CharField(u'欢迎语', max_length=1000)
    #1代表已删除或者过期,0代表未开始，2代表正在进行
    begin_time = models.DateTimeField(u'起始时间')
    end_time = models.DateTimeField(u'结束时间')
    flag_status = models.CharField(u"状态", max_length=100)
    flag_check = models.CharField(u"审核", max_length=25)
    anonymity = models.CharField(u'匿名', max_length=25) 
    class Meta:
        db_table = "wall_item"
        app_label = 'wall'


class WallUser(models.Model):
    wx = models.ForeignKey(WXAccount, verbose_name = u'微信账号')
    openid = models.CharField('OpenID', max_length=255)
    nickname = models.CharField(u'用户昵称', max_length=255, blank=True)
    pic = models.CharField(u'用户头像', max_length=255, blank=True)
    create_time = models.DateTimeField(u'关注时间', auto_now_add=True)
    #0代表未上墙
    wall_item_id = models.CharField(u'活动id', max_length=100, blank=True)

    class Meta:
        db_table = "wall_user"
        app_label = 'wall'

class WallMsg(models.Model):
    user = models.ForeignKey(WallUser, verbose_name=u'微信用户')
    type = models.CharField(u'类型', max_length=100)
    content = models.TextField(u"消息内容")
    create_time = models.DateTimeField(u'时间', auto_now_add=True)
    #0 presents new, 1 presents pass, 2 presents not pass
    flag_pass = models.IntegerField(u'审核状态', default=0)
    pass_time = models.DateTimeField(u'审核时间', auto_now=True, auto_now_add=True)
    #1 prensents 已显示在墙上
    flag_show = models.IntegerField(u'显示状态', default=0)
    #1 presents 已发布
    flag_on = models.IntegerField(u'发布状态', default=0)
    wall_item_id = models.CharField(u"活动墙序号", max_length=100)

    class Meta:
        db_table = "wall_msg"
        app_label = 'wall'

class WallAccesstoken(models.Model):
    wx = models.ForeignKey(WXAccount, verbose_name = u'微信账号')
    access_token = models.CharField(u'accessToken', max_length=255, blank=True)
    last_get_time = models.DateTimeField(u'上次获取时间', auto_now_add=True)
    app_id = models.CharField(u'AppId', max_length=255, blank=True, null=True)
    app_secret = models.CharField(u'AppSecret', max_length=255, blank=True, null=True)

    class Meta:
        db_table = "wall_accesstoken"
        app_label = 'wall'
