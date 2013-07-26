#coding:utf8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User)
    qq = models.CharField(u'QQ', max_length = 20)
    status = models.IntegerField(u'账户类型')
    endtime = models.DateTimeField(u'付费终止时间')

    class Meta:
        db_table = u"account"
        app_label = "account"

class Weixin(models.Model):
    account = models.ForeignKey(Account, verbose_name = u'系统账号')
    name = models.CharField(u"微信帐户名", max_length=20)
    status = models.IntegerField(u'微信账户状态')
    addtime = models.DateTimeField(u'绑定时间')
    max_msg_cnt = models.IntegerField(u'最大消息数目')
    class Meta:
        db_table = u"mp_account"
        app_label = 'account'
 


