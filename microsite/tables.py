#coding:utf8
from models import HomePage
import django_tables2 as tables
from django.contrib.contenttypes.models import ContentType
from models import ContactApp, TrendsApp, ContactItem, TrendItem, ContactPeople, CaseItem, CaseClass, ProductItem, ProductClass, Menu
from django_tables2.columns import DateTimeColumn, TemplateColumn

class HomePageTable(tables.Table):
    class Meta:
        model = HomePage
        attrs = {'class' : 'table table-striped'}
        orderable = False

class ContactTable(tables.Table):
    ops = TemplateColumn(template_name="contact_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ContactItem
        order_by = 'pk'
        empty_text = u'暂无联系方式'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('name', 'address', 'fax_code')

class ContactPeopleTable(tables.Table):
    ops = TemplateColumn(template_name="contact_people_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ContactPeople
        order_by = 'pk'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        empty_text = u'暂无联系人'
        fields = ('name', 'email', 'phone', 'qq')


class TrendsTable(tables.Table):
    ops = TemplateColumn(template_name="trend_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = TrendItem
        order_by = 'pub_time'
        empty_text = u'暂无公司动态'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('title', 'pub_time', 'summary')

class CaseItemTable(tables.Table):
    ops = TemplateColumn(template_name="case_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = CaseItem
        order_by = 'pub_time'
        empty_text = u'暂无案例'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('title', 'cls')


class CaseClassTable(tables.Table):
    ops = TemplateColumn(template_name="case_class_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = CaseClass
        order_by = 'pub_time'
        empty_text = u'暂无案例分类'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('name',)
    
class ProductItemTable(tables.Table):
    ops = TemplateColumn(template_name="product_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ProductItem
        order_by = 'pub_time'
        empty_text = u'暂无产品'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('title', 'cls')


class ProductClassTable(tables.Table):
    ops = TemplateColumn(template_name="product_class_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = ProductClass
        order_by = 'pub_time'
        empty_text = u'暂无案例分类'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('name',)

class MenuTable(tables.Table):
    ops = TemplateColumn(template_name="menu_ops.html", verbose_name=u"操作", orderable=False,attrs={"class":"ops"})
    class Meta:
        model = Menu
        empty_text = u'暂无菜单项'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('name', 'page.tab_name',)
