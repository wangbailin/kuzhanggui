#coding:utf-8
from django.db import models
from framework.models import WXAccount
import datetime

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
    def save(self, *args, **kwargs):
        self.date_str = self.date.strftime("%Y-%m-%d")
        super(WeixinDailyData, self).save(args, kwargs)

    @classmethod
    def today_subscribe_one(cls, wx_id):
        wx_account = WXAccount.objects.get(id=wx_id)
        wx_account.follower_count += 1
        wx_account.save()
        try:
            today_data = WeixinDailyData.objects.get(weixin=wx_account, date=datetime.date.today())
        except:
            today_data = WeixinDailyData()
            today_data.weixin = wx_account
            today_data.date = datetime.date.today()

        today_data.follow_count += 1
        today_data.new_count += 1
        today_data.save()
    
    @classmethod
    def today_unsubscribe_one(cls, wx_id):
        wx_account = WXAccount.objects.get(id=wx_id)
        wx_account.follower_count -= 1
        wx_account.save()
        try:
            today_data = WeixinDailyData.objects.get(weixin=wx_account, date=datetime.date.today())
        except:
            today_data = WeixinDailyData()
            today_data.weixin = wx_account
            today_data.date = datetime.date.today()

        today_data.unfollow_count -= 1
        today_data.new_count -= 1
        today_data.save()

class WSiteDailyData(models.Model):
    weixin = models.ForeignKey(WXAccount)
    date = models.DateField(auto_now_add=True)
    date_str = models.CharField(max_length=20)
    visitor_count = models.BigIntegerField(u'访问人数', default=0)
    visit_count = models.IntegerField(u'访问次数', default=0)

    class Meta:
        db_table = u'd_wsite_daily'

    def save(self, *args, **kwargs):
        self.date_str = self.date.strftime("%Y-%m-%d")
        super(WSiteDailyData, self).save(args, kwargs)

    @classmethod
    def today(cls, wx_id, pv, uv):
        wx_account = WXAccount.objects.get(id=wx_id)
        try:
            today_data = WSiteDailyData.objects.get(weixin=wx_account, date=datetime.date.today())
        except:
            today_data = WSiteDailyData()
            today_data.weixin = wx_account;
            today_data.date = datetime.date.today()

        today_data.visitor_count = uv
        today_data.visit_count = pv
        today_data.save()
