#coding:utf8
from django.db import models

# Create your models here.
class Account(models.Model):
    phone = models.CharField(u'手机号', max_length=20)
    password = models.CharField(u'密码', max_length=100)
    email = models.CharField(u'邮箱', max_length = 50)
    qq = models.CharField(u'QQ', max_length = 20)
    reg_time = models.DateTimeField(u"注册时间", auto_now_add = True)
    last_login_time = models.DateTimeField(u"上一次登陆时间")

    class Meta:
        db_table = u"company"
        app_label = "account"

class Weixin(models.Model):
    company = models.ForeignKey(Account, verbose_name = u'公司')
    wx_account = models.CharField(u'微信账号', max_length=50)
    wx_pwd = models.CharField(u'微信密码', max_length=50)
    status = models.IntegerField(u'微信账户状态')
    class Meta:
        db_table = u"weixin"
        app_label = 'account'
 


