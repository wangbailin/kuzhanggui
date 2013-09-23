#coding:utf8
from models import HomePage
import django_tables2 as tables
from django.contrib.contenttypes.models import ContentType
from models import ContactApp, TrendsApp, ContactItem, TrendItem, TeamItem, ContactPeople, CaseItem, CaseClass, ProductItem, ProductClass, Menu
from django_tables2.columns import DateTimeColumn, TemplateColumn

class HomePageTable(tables.Table):
    class Meta:
        model = HomePage
        attrs = {'class' : 'table table-striped'}
        orderable = False

class ContactTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="contact_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ContactItem
        order_by = '-id'
        empty_text = u'暂无联系地址'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('name', 'address', 'fax_code')

class ContactPeopleTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="contact_people_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ContactPeople
        order_by = '-id'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        empty_text = u'暂无联系人'
        fields = ('contact_item', 'name', 'email', 'phone', 'qq')


class TrendsTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="trend_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = TrendItem
        order_by = '-id'
        empty_text = u'暂无公司动态'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('title', 'pub_time', 'summary')

class TeamTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="team_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = TeamItem
        empty_text = u'暂无团队成员介绍'
        order_by = '-id'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name', 'job_title', 'person_digest')

class CaseItemTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="case_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = CaseItem
        order_by = '-id'
        empty_text = u'暂无成功案例'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('title', 'cls')


class CaseClassTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="case_class_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = CaseClass
        order_by = '-id'
        empty_text = u'暂无案例分类'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name',)
    
class ProductItemTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="product_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ProductItem
        order_by = '-id'
        empty_text = u'暂无产品'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('title', 'cls')


class ProductClassTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="product_class_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ProductClass
        order_by = '-id'
        empty_text = u'暂无产品分类'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name',)

class MenuTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="menu_ops.html", verbose_name=u"操作", orderable=False,attrs={"class":"ops"})
    class Meta:
        model = Menu
        order_by = '-id'
        empty_text = u'暂无菜单项'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('name', 'page.tab_name',)
