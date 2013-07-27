#coding:utf8
from django.db import models

from account.models import Weixin

class Page(models.Model):
    real_type = models.ForeignKey(ContentType, editable=False)
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    tab_name = models.CharField(u'tab的名字')

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
            self.tab_name = self._get_tab_name()
        super(InheritanceCastModel, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    def _get_tab_name(self):
        raise NotImplementedError

    class Meta:
        abstract = True

# Create your models here.
class HomePage(Page):
    name = models.CharField(u'官网名称', max_length=50)
    template_type = models.IntegerField(u'模板类型')
    pic1 = models.ImageField(u"焦点图1", upload_to='upload/', max_length=255, blank=True)
    pic2 = models.ImageField(u"焦点图2", upload_to='upload/', max_length=255, blank=True)
    pic3 = models.ImageField(u"焦点图3", upload_to='upload/', max_length=255, blank=True)
    pic4 = models.ImageField(u"焦点图4", upload_to='upload/', max_length=255, blank=True)
    cover = models.ImageField(u"消息封面", upload_to='upload/', max_length=255, blank=True)
    content = models.CharField(u"内容", max_length=1000)

    def _get_tab_name(self):
        return u"首页"

    class Meta:
        db_table = u"homepage"
        app_label = u'microsite'

class IntroPage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=50)
    content = models.TextField(u'内容')

    class Meta:
        db_table = u"intropage"
        app_label = u'microsite'

    def _get_tab_name(self):
        return u"公司简介"

class JoinPage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=50)
    content = models.TextField(u'内容')

    def _get_tab_name(self):
        return u"加入我们"

    class Meta:
        db_table = u'joinpage'
        app_label = u'microsite'

class ConnectPage(Page):
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    enable = models.BooleanField(u'是否启用', default = True)

    def _get_tab_name(self):
        return u"联系我们"

    class Meta:
        db_table = u'connectpage'
        app_label = u'micosite'

class TrendsPage(Page):
    wx = models.ForeignKey(Weixin, verbose_name = u'微信账号')
    enable = models.BooleanField(u'是否启用')

    def _get_tab_name(self):
        return u"公司动态"

    class Meta:
        db_table = u"trendspage"
        app_label = u'microsite'
    
class TrendItem(models.Model):
    trend = models.ForeignKey(TrendsPage, verbose_name = u'趋势')
    pub_time = models.DateField(u'日期')
    content = models.CharField(u'内容', max_length=1000)

    class Meta:
        db_table = u"trend_item"
        app_label = u'microsite'

class ConnectItem(models.Model):
    connect = models.ForeignKey(ConnectPage, verbose_name = u'联系我们')
    name = models.CharField(u'公司名称', max_length=50)
    address = models.CharField(u'公司地址', max_length=200)
    mail_code = models.CharField(u'邮政编码', max_length=20)
    fax_code = models.CharField(u'传真号码', max_length=30)

    class Meta:
        db_table = u'connect_item'
        app_label = u'microsite'

class ConnectPeople(models.Model):
    connect_item = models.ForeignKey(ConnectItem, verbose_name = u'联系方式')
    name = models.CharField(u'联系人', max_length=10)
    email = models.CharField(u'联系邮箱', max_length=50)
    phone = models.CharField(u'联系电话', max_length=20)
    qq = models.CharField(u'QQ', max_length=20)

    class Meta:
        db_table = u'connect_people'
        app_label = u'microsite'
