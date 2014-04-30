#coding:utf8
import logging
from models import HomePage, PageGroup
import django_tables2 as tables
import django_tables2 as tables
from django.contrib.contenttypes.models import ContentType
from models import ContactApp, JoinApp, TrendsApp, ContactItem, JoinItem, TrendItem, TeamItem, ContactPeople, CaseItem, CaseClass, ProductItem, ProductClass, Menu
from django_tables2.columns import DateTimeColumn, TemplateColumn
from django.utils.safestring import mark_safe

logger = logging.getLogger("default")

class HomePageTable(tables.Table):
    class Meta:
        model = HomePage
        attrs = {'class' : 'table table-striped'}
        orderable = False

class ContactTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="contact_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = ContactItem
        order_by = '-position'
        empty_text = u'暂无联系地址'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('name', 'address', 'fax_code', 'position')

class ContactPeopleTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="contact_people_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = ContactPeople
        order_by = '-position'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        empty_text = u'暂无联系人'
        fields = ('contact_item', 'name', 'email', 'phone', 'qq', 'position')

class JoinTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="join_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)

    def render_publish(self, record):
        icon = "icon-ok" if record.publish else "icon-remove"
        return mark_safe("<i class='" + icon + "'></i>")

    class Meta:
        model = JoinItem
        order_by = '-position'
        empty_text = u'暂无职位'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('job_title', 'publish', 'pub_time', 'position' )

class TrendsTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="trend_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = TrendItem
        order_by = '-position'
        empty_text = u'暂无新闻'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('title','pub_time','summary', 'position')

class TeamTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="team_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = TeamItem
        empty_text = u'暂无教师'
        order_by = 'position'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name', 'person_digest','position')

class CaseItemTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="case_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = CaseItem
        order_by = '-position'
        empty_text = u'暂无成功案例'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('title', 'cls', 'position')


class CaseClassTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="case_class_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = CaseClass
        order_by = '-position'
        empty_text = u'暂无案例分类'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name', 'position')

class ProductItemTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="product_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = ProductItem
        order_by = '-position'
        empty_text = u'暂无课程'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('title', 'cls', 'position')


class ProductClassTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    ops = TemplateColumn(template_name="product_class_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    position = tables.Column(orderable=True)
    class Meta:
        model = ProductClass
        order_by = '-position'
        empty_text = u'暂无课程分类'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name', 'position')

class MenuTable(tables.Table):
    pages = TemplateColumn(template_name="menu_pages.html", verbose_name=u'页面')
    ops = TemplateColumn(template_name="menu_ops.html", verbose_name=u"操作", orderable=False,attrs={"class":"ops"})

    class Meta:
        model = Menu
        empty_text = u'暂无菜单项'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name',)
