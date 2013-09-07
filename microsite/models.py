#coding:utf8
from django.db import models
from django.contrib.contenttypes.models import ContentType

from site_template import site_templates
from framework.models import WXAccount

from ckeditor.fields import RichTextField

from rocket import settings
from microsite import consts

class Page(models.Model):
    real_type = models.ForeignKey(ContentType, editable=False)
    wx = models.ForeignKey(WXAccount, verbose_name = u'微信账号')
    tab_name = models.CharField(u'页面名称', max_length=20)
    template_name = models.CharField(u'template的文件路径', max_length=260)
    message_cover = models.ImageField(u"消息封面", upload_to='upload/', help_text=u"微信返回消息的封面，建议图片宽度大于640像素", max_length=255, blank=True)
    message_description = models.TextField(u"消息内容", help_text=u"微信返回消息的内容", max_length=1000, blank=True)

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

    def get_url(self):
        raise NotImplementedError

    class Meta:
        db_table = 'page'
        app_label = 'microsite'

    def __unicode__(self):
        return self.tab_name

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
    exp1 = models.CharField(u"焦点图1注释", max_length=255, blank=True)
    pic2 = models.ImageField(u"焦点图2", upload_to='upload/', max_length=255, blank=True)
    exp2 = models.CharField(u"焦点图2注释", max_length=255, blank=True)
    pic3 = models.ImageField(u"焦点图3", upload_to='upload/', max_length=255, blank=True)
    exp3 = models.CharField(u"焦点图3注释", max_length=255, blank=True)
    pic4 = models.ImageField(u"焦点图4", upload_to='upload/', max_length=255, blank=True)
    exp4 = models.CharField(u"焦点图4注释", max_length=255, blank=True)

    def _get_tab_name(self):
        return u"首页"

    def _get_template(self):
        return 'homepage.html'

    def get_url(self):
        return '/microsite/homepage/%d' % self.pk

    class Meta:
        db_table = u"homepage"
        app_label = u'microsite'


class IntroPage(Page):
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用")
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

    def get_url(self):
        return '/microsite/intro/%d' % self.pk

class JoinPage(Page):
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用")
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

    def get_url(self):
        return '/microsite/join/%d' % self.pk

    class Meta:
        db_table = u'joinpage'
        app_label = u'microsite'

class ContactApp(App):
    enable = models.BooleanField(u'是否启用', help_text=u"启用")
    title = models.CharField(u'标题', max_length=50) 

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '联系我们'
        super(ContactApp, self).save(*args, **kwargs)

    def _get_tab_name(self):
        return self.title

    def _get_app_template(self):
        return 'contact_app.html'

    def get_url(self):
        return '/microsite/contact/%d' % self.pk

    class Meta:
        db_table = u'contactapp'
        app_label = u'microsite'


class TrendsApp(App):
    enable = models.BooleanField(u'是否启用', help_text=u"启用")
    title = models.CharField(u'标题', max_length=50)
 
    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '公司动态'
        super(TrendsApp, self).save(*args, **kwargs)


    def _get_tab_name(self):
        return self.title

    def _get_app_template(self):
        return 'trends_app.html'

    def get_url(self):
        return '/microsite/trend/%d' % self.pk

    class Meta:
        db_table = u"trendsapp"
        app_label = u'microsite'

class CaseApp(App):
    enable = models.BooleanField(u'是否启用', help_text=u"启用")
    title = models.CharField(u'标题', max_length=20)

    def _get_tab_name(self):
        if len(self.title) > 0:
            return self.title
        else:
            return u'案例中心'

    def _get_app_template(self):
        return 'case_app.html'

    def get_url(self):
        return '/microsite/case/%d' % self.pk

    class Meta:
        db_table = u'case_app'
        app_label = u'microsite'

class CaseClass(models.Model):
    case_app = models.ForeignKey(CaseApp, verbose_name=u'案例')
    name = models.CharField(u'分类名称', max_length=20)
    pub_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    
    class Meta:
        db_table = u'case_class'        
        app_label = u'microsite'

    def get_url(self):
        return '/microsite/case/%d/%d' % (self.case_app.id, self.pk)

    def __unicode__(self):
        return self.name

class CaseItem(models.Model):
    case_app = models.ForeignKey(CaseApp, verbose_name=u'案例')
    cls = models.ForeignKey(CaseClass, verbose_name=u'分类')
    pub_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    title = models.CharField(u'案例名称', max_length=100)
    case_pic1 = models.ImageField(u"案例截图1", upload_to='upload/', max_length=255, blank=True)
    case_pic2 = models.ImageField(u"案例截图2", upload_to='upload/', max_length=255, blank=True)
    case_pic3 = models.ImageField(u"案例截图3", upload_to='upload/', max_length=255, blank=True)
    case_pic4 = models.ImageField(u"案例截图4", upload_to='upload/', max_length=255, blank=True)
    case_intro = models.TextField(u"案例介绍")

    class Meta:
        db_table = u'case_item'
        app_label = u'microsite'

class ProductApp(App):
    enable = models.BooleanField(u'是否启用', help_text=u"启用")
    title = models.CharField(u'标题', max_length=20)

    def _get_tab_name(self):
        if len(self.title) > 0:
            return self.title
        else:
            return u'产品中心'

    def _get_app_template(self):
        return 'product_app.html'

    def get_url(self):
        return '/microsite/product/%d' % self.pk

    class Meta:
        db_table = u'product_app'
        app_label = u'microsite'

class ProductClass(models.Model):
    product_app = models.ForeignKey(ProductApp, verbose_name=u'产品')
    name = models.CharField(u'分类名称', max_length=20)
    pub_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    
    class Meta:
        db_table = u'product_class'        
        app_label = u'microsite'

    def get_url(self):
        return '/microsite/product/%d/%d' % (self.product_app.id, self.pk)

    def __unicode__(self):
        return self.name

class ProductItem(models.Model):
    product_app = models.ForeignKey(ProductApp, verbose_name=u'产品')
    cls = models.ForeignKey(ProductClass, verbose_name=u'分类')
    pub_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    title = models.CharField(u'产品名称', max_length=100)
    product_pic1 = models.ImageField(u"产品截图1", upload_to='upload/', max_length=255, blank=True)
    product_pic2 = models.ImageField(u"产品截图2", upload_to='upload/', max_length=255, blank=True)
    product_pic3 = models.ImageField(u"产品截图3", upload_to='upload/', max_length=255, blank=True)
    product_pic4 = models.ImageField(u"产品截图4", upload_to='upload/', max_length=255, blank=True)
    product_intro = models.TextField(u"产品介绍")

    class Meta:
        db_table = u'product_item'
        app_label = u'microsite'


    
class TrendItem(models.Model):
    trend = models.ForeignKey(TrendsApp, verbose_name = u'趋势')
    pub_time = models.DateField(u'日期')
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容')
    cover = models.ImageField(u'封面', upload_to='upload/', max_length=255, blank=True)
    summary = models.CharField(u'摘要', max_length=255, blank=True)

    class Meta:
        db_table = u"trend_item"
        app_label = u'microsite'

class ContactItem(models.Model):
    contact = models.ForeignKey(ContactApp, verbose_name = u'联系我们')
    name = models.CharField(u'公司名称', max_length=50)
    lat = models.FloatField(u'公司纬度')
    lng = models.FloatField(u'公司经度')
    address = models.CharField(u'公司地址', max_length=200)
    mail_code = models.CharField(u'邮政编码', max_length=20, blank=True)
    fax_code = models.CharField(u'传真号码', max_length=30, blank=True)

    class Meta:
        db_table = u'contact_item'
        app_label = u'microsite'
    def __unicode__(self):
        return self.name

class ContactPeople(models.Model):
    contact_item = models.ForeignKey(ContactItem, verbose_name = u'公司名称')
    name = models.CharField(u'联系人', max_length=10)
    email = models.CharField(u'联系邮箱', max_length=50, blank=True)
    phone = models.CharField(u'联系电话', max_length=20)
    qq = models.CharField(u'QQ', max_length=20, blank=True)

    class Meta:
        db_table = u'contact_people'
        app_label = u'microsite'

class CulturePage(Page):
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用")
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容')

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '公司文化'
        super(CulturePage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"culture"
        app_label = u'microsite'

    def get_url(self):
        return '/microsite/culture/%d' % self.pk

    def _get_template(self):
        return 'intropage.html'
    def _get_tab_name(self):
        return self.title

class BusinessPage(Page):
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用")
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容')

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '公司业务'
        super(BusinessPage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"business"
        app_label = u'microsite'

    def get_url(self):
        return '/microsite/business/%d' % self.pk

    def _get_template(self):
        return 'intropage.html'

    def _get_tab_name(self):
        return self.title


class WeiboPage(Page):
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用")
    title = models.CharField(u'标题', max_length=100)
    url = models.URLField(u"微博链接", max_length=100)

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
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用")
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
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用")
    title = models.CharField(u'标题', max_length=100)
    icon = models.ImageField(u'首页图标', upload_to='upload/', max_length=255)
    url = models.URLField(u'链接地址', max_length=200)
    
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

    def get_url(self):
        return '/microsite/link/%d' % self.pk

class Menu(models.Model):
    wx = models.ForeignKey(WXAccount, verbose_name=u'微信帐号')
    name = models.CharField(verbose_name=u'菜单项名称', max_length=4, blank=False, null=False)
    page = models.ForeignKey(Page, verbose_name=u'页面')

    class Meta:
        db_table = u'menus'
        app_label = u'microsite'

    def __unicode__(self):
        return self.page.tab_name

def add_default_site(wx_account):
    homepages = HomePage.objects.filter(wx=wx_account)
    if len(homepages) == 0:
        homepage = HomePage()
        homepage.wx = wx_account
        homepage.name = wx_account.name
        homepage.message_description = consts.DEFAULT_HOMEPAGE_MSG % wx_account.name
        homepage.template_type = 0
        homepage.save()

    intropages = IntroPage.objects.filter(wx=wx_account)
    if len(intropages) == 0:
        intropage = IntroPage()
        intropage.wx = wx_account
        intropage.enable = True
        intropage.title = u"公司简介"
        intropage.message_description = consts.DEFAULT_INTRO_MSG
        intropage.save()

    businesspages = BusinessPage.objects.filter(wx=wx_account)
    if len(businesspages) == 0:
        businesspage = BusinessPage()
        businesspage.wx = wx_account
        businesspage.enable = True
        businesspage.title = '公司业务'
        businesspage.message_description = consts.DEFAULT_BUSINESS_MSG
        businesspage.save()

    trendsapps = TrendsApp.objects.filter(wx=wx_account)
    if len(trendsapps) == 0:
        trendsapp = TrendsApp()
        trendsapp.wx = wx_account
        trendsapp.enable = True
        trendsapp.message_cover = consts.DEFAULT_NEWS_COVER
        trendsapp.message_description = consts.DEFAULT_NEWS_MSG
        trendsapp.save()

    joinpages = JoinPage.objects.filter(wx=wx_account)
    if len(joinpages) == 0:
        joinpage = JoinPage()
        joinpage.wx = wx_account
        joinpage.enable = True
        joinpage.title = u'加入我们'
        joinpage.message_cover = consts.DEFAULT_JOIN_COVER
        joinpage.message_description = consts.DEFAULT_JOIN_MSG
        joinpage.save()

    contactapps = ContactApp.objects.filter(wx=wx_account)
    if len(contactapps) == 0:
        contactapp = ContactApp()
        contactapp.wx = wx_account
        contactapp.enable = True
        contactapp.message_cover = consts.DEFAULT_CONTACT_COVER
        contactapp.message_description = consts.DEFAULT_CONTACT_MSG
        contactapp.save()

    caseapps = CaseApp.objects.filter(wx=wx_account)
    if len(caseapps) == 0:
        caseapp = CaseApp()
        caseapp.wx = wx_account
        caseapp.enable = True
        caseapp.title = u'成功案例'
        caseapp.message_cover = consts.DEFAULT_CASE_COVER
        caseapp.message_description = consts.DEFAULT_CASE_MSG
        caseapp.save()

    productapps = ProductApp.objects.filter(wx=wx_account)
    if len(productapps) == 0:
        productapp = ProductApp()
        productapp.wx = wx_account
        productapp.enable = True
        productapp.title = u'产品中心'
        productapp.message_cover = consts.DEFAULT_PRODUCT_COVER
        productapp.message_description = consts.DEFAULT_PRODUCT_MSG
        productapp.save()
    
    weibopages= WeiboPage.objects.filter(wx=wx_account)
    if len(weibopages) == 0:
        weibopage = WeiboPage()
        weibopage.wx = wx_account
        weibopage.enable = True
        weibopage.title = u'官方微博'
        weibopage.message_description = consts.DEFAULT_WEIBO_MSG
        weibopage.save()

def get_page_url(page):
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        return '/microsite/contact/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return '/microsite/trend/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        return '/microsite/case/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        return '/microsite/product/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(HomePage):
        return '/microsite/homepage/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return '/microsite/intro/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return '/microsite/business/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(JoinPage):
        return '/microsite/join/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        weibo = page.cast()
        return weibo.url
    elif page.real_type == ContentType.objects.get_for_model(ContentPage):
        return '/microsite/content/%d' % page.id
    elif page.real_type == ContentType.objects.get_for_model(LinkPage):
        return '/microsite/link/%d' % page.id

def get_default_msg(page):
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        return consts.DEFAULT_CONTACT_MSG
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return consts.DEFAULT_NEWS_MSG
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        return consts.DEFAULT_CASE_MSG
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        return consts.DEFAULT_PRODUCT_MSG
    elif page.real_type == ContentType.objects.get_for_model(HomePage):
        return consts.DEFAULT_HOMEPAGE_MSG
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return consts.DEFAULT_INTRO_MSG
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return consts.DEFAULT_BUSINESS_MSG
    elif page.real_type == ContentType.objects.get_for_model(JoinPage):
        return consts.DEFAULT_JOIN_MSG
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        return consts.DEFAULT_WEIBO_MSG
    elif page.real_type == ContentType.objects.get_for_model(ContentPage):
        return consts.DEFAULT_MSG
    elif page.real_type == ContentType.objects.get_for_model(LinkPage):
        return consts.DEFAULT_MSG

def get_default_cover(page):
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        return consts.DEFAULT_CONTACT_COVER
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return consts.DEFAULT_NEWS_COVER
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        return consts.DEFAULT_CASE_COVER
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        return consts.DEFAULT_PRODUCT_COVER
    elif page.real_type == ContentType.objects.get_for_model(HomePage):
        return consts.DEFAULT_COVER
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return consts.DEFAULT_COVER
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return consts.DEFAULT_COVER
    elif page.real_type == ContentType.objects.get_for_model(JoinPage):
        return consts.DEFAULT_JOIN_COVER
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        return consts.DEFAULT_COVER
    elif page.real_type == ContentType.objects.get_for_model(ContentPage):
        return consts.DEFAULT_COVER
    elif page.real_type == ContentType.objects.get_for_model(LinkPage):
        return consts.DEFAULT_COVER
