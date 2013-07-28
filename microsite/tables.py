#coding:utf8
from models import HomePage
import django_tables2 as tables
from django.contrib.contenttypes.models import ContentType
from models import ContactApp, TrendsApp, ContactItem, TrendItem, ContactPeople
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
        empty_text = u'暂无联系方式，快点添加吧'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('name', 'address', 'mail_code', 'fax_code')

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
        empty_text = u'暂无公司动态，快点添加，让听众了解公司的最新状况'
        attrs = {'class' : 'table table-striped'}
        orderable = False
        fields = ('title', 'pub_time', 'content')


class TableManager():
    @classmethod
    def get_table(cls, app):
        if app.real_type == ContentType.objects.get_for_model(ContactApp):
            return ContactTable(ContactItem.objects.all())
        elif app.real_type == ContentType.objects.get_for_model(TrendsApp):
            return TrendsTable(TrendItem.objects.all())
        else:
            raise Exception("bad real type")
