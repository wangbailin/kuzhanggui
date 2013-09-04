# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
	user = models.OneToOneField(User)

	qq = models.CharField(u'QQ', max_length = 20, blank = True, null = True)
	phone = models.CharField(u'手机号码', max_length = 20)
	expired_time = models.DateTimeField(u'过期时间')
	is_expired = models.BooleanField(u'是否过期', default=False)
	has_wx_bound = models.BooleanField(u'绑定微信公众号', default=False)

	class Meta:
		db_table = u'account'

class WXAccount(models.Model):
	account = models.ForeignKey(Account)

	name = models.CharField(u'名称', max_length=20, blank=True, null=True)
	avatar = models.ImageField(u'图标', upload_to='avatar/', max_length=255, blank=True)
	follower_count = models.IntegerField(u'粉丝数量', max_length=11, default=0)
	message_count = models.IntegerField(u'消息数量', max_length=11, default=0)

	username = models.CharField(u'用户名', max_length=255, blank=True, null=True)
	STATE_UNBOUND = 1
	STATE_BINDING = 2
	STATE_BOUND_UNCHECKED = 3
	STATE_BOUND = 4
	STATE_CHOICES = (
		(STATE_UNBOUND, u'未绑定'),
		(STATE_BINDING, u'绑定中'),
		(STATE_BOUND_UNCHECKED, '未验证'),
		(STATE_BOUND, u'绑定成功'))
	state = models.IntegerField(u'状态', max_length=2, choices=STATE_CHOICES, default=STATE_UNBOUND)
	url = models.CharField(u'URL', max_length=255)
	token = models.CharField(u'Token', max_length=255)
	wxid = models.CharField(u'WXID', max_length=255, blank=True, null=True)
	bind_time = models.DateTimeField(u'绑定时间', blank=True, null=True)
	app_id = models.CharField(u'AppId', max_length=255, blank=True, null=True)
	app_secret = models.CharField(u'AppSecret', max_length=255, blank=True, null=True)

	class Meta:
		db_table = u"wx_account"