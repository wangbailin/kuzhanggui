#coding:utf-8
from django.db import models
from framework.models import WXAccount

class WeixinDailyData(models.Model):
    weixin = models.ForeignKey(WXAccount)
    date = models.DateField(auto_now_add=True)
    date_str = models.CharField(max_length=20)
    follow_count = models.IntegerField(u'关注', default=0)
    unfollow_count = models.IntegerField(u'取消关注', default=0)
    new_count = models.IntegerField(u'新增粉丝', default=0)
    msg_count = models.IntegerField(default=0)

    class Meta:
        db_table = u'd_weixin_daily'

class WSiteDailyData(models.Model):
    weixin = models.ForeignKey(WXAccount)
    date = models.DateField(auto_now_add=True)
    date_str = models.CharField(max_length=20)
    visitor_count = models.BigIntegerField(u'访问人数', default=0)
    visit_count = models.IntegerField(u'访问次数', default=0)

    class Meta:
        db_table = u'd_wsite_daily'