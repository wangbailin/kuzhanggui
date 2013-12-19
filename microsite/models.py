#coding:utf8
import sys
from django.db import models, connection
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from site_template import site_templates
from framework.models import WXAccount

from ckeditor.fields import RichTextField

from rocket import settings
from microsite import consts
from baidu_yun.storage import BaiduYunStorage

baidu_storage = BaiduYunStorage()

class Page(models.Model):
    enable = models.BooleanField(u'是否启用', default = True, help_text=u"启用 (启用后该页面内容会显示在微官网)")
    real_type = models.ForeignKey(ContentType, editable=False)
    wx = models.ForeignKey(WXAccount, verbose_name = u'微信账号')
    tab_name = models.CharField(u'页面名称', max_length=20)
    template_name = models.CharField(u'template的文件路径', max_length=260)
    icon = models.ImageField(u"图标", storage=baidu_storage, upload_to='upload/', help_text=u"建议图片大小为190px*235px", max_length=255, blank=True)
    message_cover = models.ImageField(u"消息封面", storage=baidu_storage, upload_to='upload/', help_text=u"微信返回消息的封面，建议图片宽度大于640像素", max_length=255, blank=True)
    message_description = models.TextField(u"消息内容", help_text=u"微信返回消息的内容", max_length=1000, blank=True)
    position = models.IntegerField(default = 0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        self.tab_name = self._get_tab_name()
        self.template_name = self._get_template()
        super(Page, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def setPosition(self, pos):
        self.position = pos

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    def _get_tab_name(self):
        raise NotImplementedError

    def _get_template(self):
        raise NotImplementedError

    def _get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return consts.DEFAULT_PRE + get_default_icon(self)

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
    pic1 = models.ImageField(u"焦点图1", storage=baidu_storage, upload_to='upload/', max_length=255)
    exp1 = models.CharField(u"焦点图1注释", max_length=255, blank=True)
    link1 = models.CharField(u"焦点图1链接页面", max_length=255, blank=True)
    pic2 = models.ImageField(u"焦点图2", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    exp2 = models.CharField(u"焦点图2注释", max_length=255, blank=True)
    link2 = models.CharField(u"焦点图2链接页面", max_length=255, blank=True)
    pic3 = models.ImageField(u"焦点图3", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    exp3 = models.CharField(u"焦点图3注释", max_length=255, blank=True)
    link3 = models.CharField(u"焦点图3链接页面", max_length=255, blank=True)
    pic4 = models.ImageField(u"焦点图4", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    exp4 = models.CharField(u"焦点图4注释", max_length=255, blank=True)
    link4 = models.CharField(u"焦点图4链接页面", max_length=255, blank=True)

    def _get_tab_name(self):
        return u"首页"

    def _get_template(self):
        return 'homepage.html'

    class Meta:
        db_table = u"homepage"
        app_label = u'microsite'


class IntroPage(Page):
    title = models.CharField(u'标题', max_length=50)
    content = models.TextField(u'内容', blank=True)

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

class JoinApp(App):
    title = models.CharField(u'标题', max_length=50)
    pic = models.ImageField(u"焦点图", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    front_words = models.TextField(u'开场语', blank=True)
    contact = models.CharField(u'联系方式', max_length=50)
    end_words = models.TextField(u'结束语', blank=True)

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '加入我们'
        super(JoinApp, self).save(*args, **kwargs)

    def _get_tab_name(self):
        return self.title

    def _get_template(self):
        return 'joinpage.html'

    def _get_app_template(self):
        return 'join_app.html'

    class Meta:
        db_table = u'joinapp'
        app_label = u'microsite'

class ContactApp(App):
    title = models.CharField(u'标题', max_length=50)

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '联系我们'
        super(ContactApp, self).save(*args, **kwargs)

    def _get_tab_name(self):
        return self.title

    def _get_app_template(self):
        return 'contact_app.html'

    class Meta:
        db_table = u'contactapp'
        app_label = u'microsite'


class TrendsApp(App):
    title = models.CharField(u'标题', max_length=50)

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '公司动态'
        super(TrendsApp, self).save(*args, **kwargs)


    def _get_tab_name(self):
        return self.title

    def _get_app_template(self):
        return 'trends_app.html'

    class Meta:
        db_table = u"trendsapp"
        app_label = u'microsite'

class TeamApp(App):
    title = models.CharField(u'标题', max_length=50)

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '团队介绍'
        super(TeamApp, self).save(*args, **kwargs)


    def _get_tab_name(self):
        return self.title

    def _get_app_template(self):
        return 'team_app.html'

    class Meta:
        db_table = u"teamapp"
        app_label = u'microsite'


class CaseApp(App):
    title = models.CharField(u'标题', max_length=20)

    def _get_tab_name(self):
        if len(self.title) > 0:
            return self.title
        else:
            return u'案例中心'

    def _get_app_template(self):
        return 'case_app.html'

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
        return settings.SITE_URL + '/microsite/case/%d/%d' % (self.case_app.id, self.pk)

    def __unicode__(self):
        return self.name

class CaseItem(models.Model):
    case_app = models.ForeignKey(CaseApp, verbose_name=u'案例')
    cls = models.ForeignKey(CaseClass, verbose_name=u'分类', blank=True, null=True)
    pub_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    title = models.CharField(u'案例名称', max_length=100)
    case_pic1 = models.ImageField(u"案例截图1", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    case_pic2 = models.ImageField(u"案例截图2", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    case_pic3 = models.ImageField(u"案例截图3", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    case_pic4 = models.ImageField(u"案例截图4", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    case_intro = models.TextField(u"案例介绍")

    class Meta:
        db_table = u'case_item'
        app_label = u'microsite'

class JoinItem(models.Model):
    join = models.ForeignKey(JoinApp, verbose_name = u'加入')
    publish = models.BooleanField(u'发布状态', default=False, help_text=u"发布")
    job_title = models.CharField(u'职位名称', max_length=100)
    number = models.IntegerField(u'招聘人数', max_length=100)
    pub_time = models.DateTimeField(u'发布时间', auto_now_add=True)
    content1 = models.TextField(u'工作内容1')
    content2 = models.TextField(u'工作内容2', blank=True)
    content3 = models.TextField(u'工作内容3', blank=True)
    content4 = models.TextField(u'工作内容4', blank=True)
    require1 = models.TextField(u'职位要求1')
    require2 = models.TextField(u'职位要求2', blank=True)
    require3 = models.TextField(u'职位要求3', blank=True)
    require4 = models.TextField(u'职位要求4', blank=True)

    class Meta:
        db_table = u"join_item"
        app_label = u'microsite'

class ProductApp(App):
    title = models.CharField(u'标题', max_length=20)

    def _get_tab_name(self):
        if len(self.title) > 0:
            return self.title
        else:
            return u'产品中心'

    def _get_app_template(self):
        return 'product_app.html'

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
        return settings.SITE_URL + '/microsite/product/%d/%d' % (self.product_app.id, self.pk)

    def __unicode__(self):
        return self.name

class ProductItem(models.Model):
    product_app = models.ForeignKey(ProductApp, verbose_name=u'产品')
    cls = models.ForeignKey(ProductClass, verbose_name=u'分类', blank=True, null=True)
    pub_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    title = models.CharField(u'产品名称', max_length=100)
    product_pic1 = models.ImageField(u"产品截图1", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    product_pic2 = models.ImageField(u"产品截图2", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    product_pic3 = models.ImageField(u"产品截图3", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    product_pic4 = models.ImageField(u"产品截图4", storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    product_intro = models.TextField(u"产品介绍")

    class Meta:
        db_table = u'product_item'
        app_label = u'microsite'



class TrendItem(models.Model):
    trend = models.ForeignKey(TrendsApp, verbose_name = u'趋势')
    pub_time = models.DateTimeField(u'日期', auto_now_add=True)
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容')
    cover = models.ImageField(u'封面', storage=baidu_storage, upload_to='upload/', max_length=255, blank=True)
    summary = models.CharField(u'摘要', max_length=255, blank=True)

    class Meta:
        db_table = u"trend_item"
        app_label = u'microsite'

class TeamItem(models.Model):
    team = models.ForeignKey(TeamApp, verbose_name = u'团队')
    pub_time = models.DateTimeField(u'日期', auto_now_add=True)
    name = models.CharField(u'姓名', max_length=100)
    job_title = models.CharField(u'职位名称', max_length=100)
    picture = models.ImageField(u"照片", storage=baidu_storage, upload_to='upload/', max_length=255)
    person_digest = models.CharField(u'简要介绍', max_length=255)
    person_content = models.TextField(u'详细介绍')

    class Meta:
        db_table = u"team_item"
        app_label = u'microsite'

class ContactItem(models.Model):
    contact = models.ForeignKey(ContactApp, verbose_name = u'联系我们')
    name = models.CharField(u'地址名称', max_length=50)
    lat = models.FloatField(u'公司纬度')
    lng = models.FloatField(u'公司经度')
    address = models.CharField(u'具体地址', max_length=200)
    mail_code = models.CharField(u'邮政编码', max_length=20, blank=True)
    fax_code = models.CharField(u'传真号码', max_length=30, blank=True)

    class Meta:
        db_table = u'contact_item'
        app_label = u'microsite'
    def __unicode__(self):
        return self.name

class ContactPeople(models.Model):
    contact_item = models.ForeignKey(ContactItem, verbose_name = u'地址名称')
    name = models.CharField(u'联系人', max_length=10)
    email = models.CharField(u'联系邮箱', max_length=50, blank=True)
    phone = models.CharField(u'联系电话', max_length=20)
    qq = models.CharField(u'QQ', max_length=20, blank=True)

    class Meta:
        db_table = u'contact_people'
        app_label = u'microsite'

class CulturePage(Page):
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容', blank=True)

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

class BusinessPage(Page):
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容', blank=True)

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '公司业务'
        super(BusinessPage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"business"
        app_label = u'microsite'

    def _get_template(self):
        return 'intropage.html'

    def _get_tab_name(self):
        return self.title


class WeiboPage(Page):
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
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容', blank=True)

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
    title = models.CharField(u'标题', max_length=100)
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

class HelpPage(Page):
    title = models.CharField(u'标题', max_length=100)
    content = models.TextField(u'内容', blank=True)

    def save(self, *args, **kwargs):
        if len(self.title) == 0:
            self.title = '新手指导'
        super(HelpPage, self).save(*args, **kwargs)

    class Meta:
        db_table = u"helppage"
        app_label = u'microsite'

    def _get_template(self):
        return 'intropage.html'

    def _get_tab_name(self):
        return self.title

class Menu(models.Model):
    wx = models.ForeignKey(WXAccount, verbose_name=u'微信帐号')
    name = models.CharField(verbose_name=u'菜单项名称', max_length=4, blank=False, null=False)

    class Meta:
        db_table = u'menus'
        app_label = u'microsite'

    def pages(self):
        pages = PageGroup.objects.filter(menu=self).order_by('position')
        result = ', '.join([p.name for p in pages])
        logger.debug("result: " + result)
        return result

    def __unicode__(self):
        return self.page.tab_name

class PageGroup(models.Model):
    menu = models.ForeignKey(Menu)
    page  = models.ForeignKey(Page)
    position = models.IntegerField(default=0)

    class Meta:
        db_table = u'menus_pages'
        app_label = u'microsite'

def add_default_site(wx_account):
    homepages = HomePage.objects.filter(wx=wx_account)
    if len(homepages) == 0:
        homepage = HomePage()
        homepage.wx = wx_account
        homepage.name = wx_account.name
        homepage.message_cover = consts.DEFAULT_HOMEPAGE_COVER
        homepage.message_description = consts.DEFAULT_HOMEPAGE_MSG % wx_account.name
        homepage.template_type = 0
        homepage.position = 0
        homepage.save()

    intropages = IntroPage.objects.filter(wx=wx_account)
    if len(intropages) == 0:
        intropage = IntroPage()
        intropage.wx = wx_account
        intropage.title = u"公司简介"
        intropage.icon = consts.DEFAULT_INTRO_ICON % site_templates[wx_account.wsite_template].site_template
        intropage.message_cover = consts.DEFAULT_INTRO_COVER
        intropage.message_description = consts.DEFAULT_INTRO_MSG
        intropage.position = 1
        intropage.save()

    businesspages = BusinessPage.objects.filter(wx=wx_account)
    if len(businesspages) == 0:
        businesspage = BusinessPage()
        businesspage.wx = wx_account
        businesspage.title = u'公司业务'
        businesspage.icon = consts.DEFAULT_BUSINESS_ICON % site_templates[wx_account.wsite_template].site_template
        businesspage.message_cover = consts.DEFAULT_BUSINESS_COVER
        businesspage.message_description = consts.DEFAULT_BUSINESS_MSG
        businesspage.position = 2
        businesspage.save()

    trendsapps = TrendsApp.objects.filter(wx=wx_account)
    if len(trendsapps) == 0:
        trendsapp = TrendsApp()
        trendsapp.wx = wx_account
        trendsapp.icon = consts.DEFAULT_NEWS_ICON % site_templates[wx_account.wsite_template].site_template
        trendsapp.message_cover = consts.DEFAULT_NEWS_COVER
        trendsapp.message_description = consts.DEFAULT_NEWS_MSG
        trendsapp.position = 3
        trendsapp.save()

    teamapps = TeamApp.objects.filter(wx=wx_account)
    if len(teamapps) == 0:
        teamapp = TeamApp()
        teamapp.wx = wx_account
        teamapp.title = u'团队介绍'
        teamapp.icon = consts.DEFAULT_TEAM_ICON % site_templates[wx_account.wsite_template].site_template
        teamapp.message_description = consts.DEFAULT_TEAM_MSG
        teamapp.position = 4
        teamapp.save()

    productapps = ProductApp.objects.filter(wx=wx_account)
    if len(productapps) == 0:
        productapp = ProductApp()
        productapp.wx = wx_account
        productapp.title = u'产品中心'
        productapp.icon = consts.DEFAULT_PRODUCT_ICON % site_templates[wx_account.wsite_template].site_template
        productapp.message_cover = consts.DEFAULT_PRODUCT_COVER
        productapp.message_description = consts.DEFAULT_PRODUCT_MSG
        productapp.position = 5
        productapp.save()

    caseapps = CaseApp.objects.filter(wx=wx_account)
    if len(caseapps) == 0:
        caseapp = CaseApp()
        caseapp.wx = wx_account
        caseapp.title = u'成功案例'
        caseapp.icon = consts.DEFAULT_CASE_ICON % site_templates[wx_account.wsite_template].site_template
        caseapp.message_cover = consts.DEFAULT_CASE_COVER
        caseapp.message_description = consts.DEFAULT_CASE_MSG
        caseapp.position = 6
        caseapp.save()

    weibopages= WeiboPage.objects.filter(wx=wx_account)
    if len(weibopages) == 0:
        weibopage = WeiboPage()
        weibopage.wx = wx_account
        weibopage.title = u'官方微博'
        weibopage.icon = consts.DEFAULT_WEIBO_ICON % site_templates[wx_account.wsite_template].site_template
        weibopage.message_cover = consts.DEFAULT_WEIBO_COVER
        weibopage.message_description = consts.DEFAULT_WEIBO_MSG
        weibopage.position = 7
        weibopage.save()

    contactapps = ContactApp.objects.filter(wx=wx_account)
    if len(contactapps) == 0:
        contactapp = ContactApp()
        contactapp.wx = wx_account
        contactapp.icon = consts.DEFAULT_CONTACT_ICON % site_templates[wx_account.wsite_template].site_template
        contactapp.message_cover = consts.DEFAULT_CONTACT_COVER
        contactapp.message_description = consts.DEFAULT_CONTACT_MSG
        contactapp.position = 8
        contactapp.save()

    joinapps = JoinApp.objects.filter(wx=wx_account)
    if len(joinapps) == 0:
        joinapp = JoinApp()
        joinapp.wx = wx_account
        joinapp.title = u'加入我们'
        joinapp.icon = consts.DEFAULT_JOIN_ICON % site_templates[wx_account.wsite_template].site_template
        joinapp.message_cover = consts.DEFAULT_JOIN_COVER
        joinapp.message_description = consts.DEFAULT_JOIN_MSG
        joinapp.position = 9
        joinapp.save()

    helppages = HelpPage.objects.filter(wx=wx_account)
    if len(helppages) == 0:
        helppage = HelpPage()
        helppage.wx = wx_account
        helppage.title = u'新手指导'
        helppage.icon = consts.DEFAULT_HELP_ICON % site_templates[wx_account.wsite_template].site_template
        helppage.message_cover = consts.DEFAULT_HELP_COVER
        helppage.message_description = consts.DEFAULT_HELP_MSG
        helppage.content = render_to_string('helppage_content.html', {})
        helppage.position = 10
        helppage.save()

def get_page_url(page):
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        return settings.SITE_URL + '/microsite/contact/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return settings.SITE_URL + '/microsite/trend/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(TeamApp):
        return settings.SITE_URL + '/microsite/team/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        return settings.SITE_URL + '/microsite/case/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        return settings.SITE_URL + '/microsite/product/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(HomePage):
        return settings.SITE_URL + '/microsite/homepage/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return settings.SITE_URL + '/microsite/intro/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return settings.SITE_URL + '/microsite/business/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(JoinApp):
        return settings.SITE_URL+ '/microsite/join/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        weibo = page.cast()
        return weibo.url
    elif page.real_type == ContentType.objects.get_for_model(HelpPage):
        return settings.SITE_URL + '/microsite/help/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(ContentPage):
        return settings.SITE_URL + '/microsite/content/%d' % (page.id)
    elif page.real_type == ContentType.objects.get_for_model(LinkPage):
        return page.cast().url

def get_item_url(item):
    if item.__class__ == JoinItem :
        return settings.SITE_URL + '/microsite/joinitem/%d' % (item.pk)
    elif item.__class__ == TrendItem:
        return settings.SITE_URL + '/microsite/trenditem/%d' % (item.pk)
    elif item.__class__ == CaseItem:
        return settings.SITE_URL + '/microsite/caseitem/%d' % (item.pk)
    elif item.__class__ == ProductItem:
        return settings.SITE_URL + '/microsite/productitem/%d' % (item.pk)

def get_default_msg(page):
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        return consts.DEFAULT_CONTACT_MSG
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return consts.DEFAULT_NEWS_MSG
    elif page.real_type == ContentType.objects.get_for_model(TeamApp):
        return consts.DEFAULT_TEAM_MSG
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
    elif page.real_type == ContentType.objects.get_for_model(JoinApp):
        return consts.DEFAULT_JOIN_MSG
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        return consts.DEFAULT_WEIBO_MSG
    elif page.real_type == ContentType.objects.get_for_model(HelpPage):
        return consts.DEFAULT_HELP_MSG
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
        return consts.DEFAULT_HOMEPAGE_COVER
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return consts.DEFAULT_INTRO_COVER
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return consts.DEFAULT_BUSINESS_COVER
    elif page.real_type == ContentType.objects.get_for_model(JoinApp):
        return consts.DEFAULT_JOIN_COVER
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        return consts.DEFAULT_WEIBO_COVER
    elif page.real_type == ContentType.objects.get_for_model(HelpPage):
        return consts.DEFAULT_HELP_COVER
    elif page.real_type == ContentType.objects.get_for_model(ContentPage):
        return consts.DEFAULT_CONTENT_COVER
    elif page.real_type == ContentType.objects.get_for_model(LinkPage):
        return consts.DEFAULT_LINK_COVER

def get_default_icon(page):
    default_icon = consts.DEFAULT_ICON
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        default_icon = consts.DEFAULT_CONTACT_ICON
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        default_icon = consts.DEFAULT_NEWS_ICON
    elif page.real_type == ContentType.objects.get_for_model(TeamApp):
        default_icon = consts.DEFAULT_TEAM_ICON
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        default_icon = consts.DEFAULT_CASE_ICON
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        default_icon = consts.DEFAULT_PRODUCT_ICON
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        default_icon = consts.DEFAULT_INTRO_ICON
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        default_icon = consts.DEFAULT_BUSINESS_ICON
    elif page.real_type == ContentType.objects.get_for_model(JoinApp):
        default_icon = consts.DEFAULT_JOIN_ICON
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        default_icon = consts.DEFAULT_WEIBO_ICON
    elif page.real_type == ContentType.objects.get_for_model(HelpPage):
        default_icon = consts.DEFAULT_HELP_ICON
    return default_icon % site_templates[page.wx.wsite_template].site_template

def get_default_title(page):
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        return u"联系我们"
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return u"公司动态"
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        return u"成功案例"
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        return u"产品中心"
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return u"公司简介"
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return u"公司业务"
    elif page.real_type == ContentType.objects.get_for_model(JoinApp):
        return u"加入我们"
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        return u"官方微博"
    elif page.real_type == ContentType.objects.get_for_model(HelpPage):
        return u"新手指导"
    elif page.real_type == ContentType.objects.get_for_model(TeamApp):
        return u"团队介绍"

def page_is_enable(subpage):
    return subpage.enable

def ensure_new_page_position(page, wx):
    pages = Page.objects.filter(wx=wx, enable=True)
    pos = len(pages)
    cursor = connection.cursor()
    cursor.execute('update page set position = position + 1 where wx_id = %s and position >= %s', (wx.pk, pos))
    page.setPosition(pos)


def set_page_enable(page):
    pages = Page.objects.filter(wx=page.wx, enable=True)
    pos = len(pages)
    cursor = connection.cursor()
    cursor.execute('update page set position = position + 1 where wx_id = %s and position >= %s and position < %s', (page.wx.pk, pos, page.position))
    page.setPosition(pos)
    page.enable = True
    page.save()

def set_page_disabled(page):
    cursor = connection.cursor()
    cursor.execute('update page set position = position - 1 where wx_id = %s and position > %s', (page.wx.pk, page.position))
    pages = Page.objects.filter(wx=page.wx).order_by('position')
    pos = len(pages) - 1
    page.setPosition(pos)
    page.enable = False
    page.save()

