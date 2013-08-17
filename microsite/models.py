#coding:utf8
from django.db import models
from django.contrib.contenttypes.models import ContentType

from site_template import site_templates
from framework.models import WXAccount

from ckeditor.fields import RichTextField

class Page(models.Model):
    real_type = models.ForeignKey(ContentType, editable=False)
    wx = models.ForeignKey(WXAccount, verbose_name = u'微信账号')
    tab_name = models.CharField(u'tab的名字', max_length=20)
    template_name = models.CharField(u'template的文件路径', max_length=260)


    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        self.tab_name = self._get_tab_name()
        self.template_name = self._get_template()
        super(Page, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    def _get_tab_name(self):
        raise NotImplementedError


    def _get_template(self):
        raise NotImplementedError

    class Meta:
        db_table = 'page'
        app_label = 'microsite'

class App(Page):
    app_template_name = models.CharField(u'template的文件路径', max_length=260)

    def save(self, *args, **kwargs):
        if not self.page_ptr_id:
            self.app_template_name = self._get_app_template()
        super(App, self).save(*args, **kwargs)

    def _get_app_template(self):
        raise NotImplementedError

    def _get_template(self):
        return 'apppage.html'

    class Meta:
        db_table = 'app'
        app_label = 'microsite'

# Create your models here.
class HomePage(Page):
    name = models.CharField(u'官网名称', max_length=50)
    choices = []
    for k,v in site_templates.items():
        choices.append( (k, v.name) )
    template_type = models.IntegerField(u'模板类型', choices=choices, default = 1)
    pic1 = models.ImageField(u"焦点图1", upload_to='upload/', max_length=255, blank=True)
    pic2 = models.ImageField(u"焦点图2", upload_to='upload/', max_length=255, blank=True)
    pic3 = models.ImageField(u"焦点图3", upload_to='upload/', max_length=255, blank=True)
    pic4 = models.ImageField(u"焦点图4", upload_to='upload/', max_length=255, blank=True)
    cover = models.ImageField(u"消息封面", upload_to='upload/', max_length=255, blank=True)
    content = models.CharField(u"内容", max_length=1000)

    def _get_tab_name(self):
        return u"首页"

    def _get_template(self):
        return 'homepage.html'

    class Meta:
        db_table = u"homepage"
        app_label = u'microsite'


class IntroPage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=50)
    content = models.TextField(u'内容')

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '公司简介'
        super(IntroPage, self).save(*args, **kwargs)
        
    class Meta:
        db_table = u"intropage"
        app_label = u'microsite'

    def _get_template(self):
        return 'intropage.html'
    def _get_tab_name(self):
        return self.title

class JoinPage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=50)
    content = models.TextField(u'内容')

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '加入我们'
        super(JoinPage, self).save(*args, **kwargs)
        
    def _get_tab_name(self):
        return self.title
    def _get_template(self):
        return 'intropage.html'

    class Meta:
        db_table = u'joinpage'
        app_label = u'microsite'

class ContactApp(App):
    enable = models.BooleanField(u'是否启用')

    def _get_tab_name(self):
        return u"联系我们"

    def _get_app_template(self):
        return 'contact_app.html'

    class Meta:
        db_table = u'contactapp'
        app_label = u'microsite'


class TrendsApp(App):
    enable = models.BooleanField(u'是否启用')

    def _get_tab_name(self):
        return u"公司动态"

    def _get_app_template(self):
        return 'trends_app.html'

    class Meta:
        db_table = u"trendsapp"
        app_label = u'microsite'
    
class TrendItem(models.Model):
    trend = models.ForeignKey(TrendsApp, verbose_name = u'趋势')
    pub_time = models.DateField(u'日期')
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容')

    class Meta:
        db_table = u"trend_item"
        app_label = u'microsite'

class ContactItem(models.Model):
    contact = models.ForeignKey(ContactApp, verbose_name = u'联系我们')
    name = models.CharField(u'公司名称', max_length=50)
    address = models.CharField(u'公司地址', max_length=200)
    mail_code = models.CharField(u'邮政编码', max_length=20, blank=True)
    fax_code = models.CharField(u'传真号码', max_length=30, blank=True)

    class Meta:
        db_table = u'contact_item'
        app_label = u'microsite'

class ContactPeople(models.Model):
    contact_item = models.ForeignKey(ContactItem, verbose_name = u'联系方式')
    name = models.CharField(u'联系人', max_length=10)
    email = models.CharField(u'联系邮箱', max_length=50, blank=True)
    phone = models.CharField(u'联系电话', max_length=20)
    qq = models.CharField(u'QQ', max_length=20, blank=True)

    class Meta:
        db_table = u'contact_people'
        app_label = u'microsite'

class CulturePage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=100)
    #content = RichTextField(u'内容')
    content = models.TextField(u'内容')

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '公司文化'
        super(CulturePage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"culture"
        app_label = u'microsite'

    def _get_template(self):
        return 'intropage.html'
    def _get_tab_name(self):
        return self.title


class WeiboPage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=100)
    url = models.CharField(u"微博链接", max_length=100)

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '官方微博'
        super(WeiboPage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"official_weibo"
        app_label = u'microsite'

    def _get_template(self):
        return 'official_weibo.html'
    def _get_tab_name(self):
        return self.title
    

class ContentPage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=100)
    icon = models.ImageField(u'首页图标', upload_to='upload/', max_length=255)
    content = models.TextField(u'内容')
    
    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '内容页面'
        super(ContentPage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"content_page"
        app_label = u'microsite'

    def _get_template(self):
        return 'content_page.html'
    def _get_tab_name(self):
        return self.title


class LinkPage(Page):
    enable = models.BooleanField(u'是否启用', default = True)
    title = models.CharField(u'标题', max_length=100)
    icon = models.ImageField(u'首页图标', upload_to='upload/', max_length=255)
    url = models.CharField(u'链接地址', max_length=200)
    
    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '链接页面'
        super(LinkPage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"link_page"
        app_label = u'microsite'

    def _get_template(self):
        return 'link_page.html'
    def _get_tab_name(self):
        return self.title
        
def add_default_site(wx_account):
    homepages = HomePage.objects.filter(wx=wx_account)
    if len(homepages) == 0:
        homepage = HomePage()
        homepage.wx = wx_account
        homepage.name = u'每日精品游戏'
        homepage.content = u'这是个好网站'
        homepage.template_type = 0
        homepage.save()

    intropages = IntroPage.objects.filter(wx=wx_account)
    if len(intropages) == 0:
        intropage = IntroPage()
        intropage.wx = wx_account
        intropage.enable = True
        intropage.title = u"我们的游戏相当好玩"
        intropage.content = u"每天一款好游戏"
        intropage.save()

    joinpages = JoinPage.objects.filter(wx=wx_account)
    if len(joinpages) == 0:
        joinpage = JoinPage()
        joinpage.wx = wx_account
        joinpage.enable = True
        joinpage.title = u'加入我们吧'
        joinpage.content = u'加入我们，奋斗吧，并享受奋斗的快感'
        joinpage.save()

    contactapps = ContactApp.objects.filter(wx=wx_account)
    if len(contactapps) == 0:
        contactapp = ContactApp()
        contactapp.wx = wx_account
        contactapp.enable = True
        contactapp.save()

    trendsapps = TrendsApp.objects.filter(wx=wx_account)
    if len(trendsapps) == 0:
        trendsapp = TrendsApp()
        trendsapp.wx = wx_account
        trendsapp.enable = True
        trendsapp.save()
    
    culturepages = CulturePage.objects.filter(wx=wx_account)
    if len(culturepages) == 0:
        culturepage = CulturePage()
        culturepage.wx = wx_account
        culturepage.enable = True
        culturepage.title = ''
        culturepage.content = 'abc'
        culturepage.save()

    weibopages= WeiboPage.objects.filter(wx=wx_account)
    if len(weibopages) == 0:
        weibopage = WeiboPage()
        weibopage.wx = wx_account
        weibopage.enable = True
        weibopage.title = ''
        weibopage.url = 'abc'
        weibopage.save()

 
