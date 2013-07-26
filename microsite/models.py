#coding:utf8
from django.db import models

from account.models import Weixin

# Create your models here.
class HomePage(models.Model):
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    name = models.CharField(u'官网名称', max_length=50)
    template_type = models.IntegerField(u'模板类型')
    pic1 = models.ImageField(u"焦点图1", upload_to='upload/', max_length=255, blank=True)
    pic2 = models.ImageField(u"焦点图2", upload_to='upload/', max_length=255, blank=True)
    pic3 = models.ImageField(u"焦点图3", upload_to='upload/', max_length=255, blank=True)
    pic4 = models.ImageField(u"焦点图4", upload_to='upload/', max_length=255, blank=True)
    cover = models.ImageField(u"消息封面", upload_to='upload/', max_length=255, blank=True)
    content = models.CharField(u"内容", max_length=1000)

    class Meta:
        db_table = u"homepage"
        app_label = u'microsite'

class IntroPage(models.Model):
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=50)
    content = models.TextField(u'内容')

    class Meta:
        db_table = u"intropage"
        app_label = u'microsite'

class JoinPage(models.Model):
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=50)
    content = models.TextField(u'内容')

    class Meta:
        db_table = u'joinpage'
        app_label = u'microsite'

class ConnectPage(models.Model):
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    enable = models.BooleanField(u'是否启用', default = True)
    
    
class TrendsPage(models.Model):
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    enable = models.BooleanField(u'启用')

    class Meta:
        db_table = u"trends"
        app_label = u'microsite'
    

class TrendItem(models.Model):
    trend = models.ForeignKey(Trends, verbose_name = u'趋势')
    pub_time = models.DateField(u'日期')
    content = models.CharField(u'内容', max_length=1000)

    class Meta:
        db_table = u"trend_item"
        app_label = u'microsite'


