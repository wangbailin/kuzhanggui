#coding:utf8
from models import WallItem
import django_tables2 as tables
from django.contrib.contenttypes.models import ContentType
from django_tables2.columns import DateTimeColumn, TemplateColumn


class WallTable(tables.Table):
    id = tables.Column(orderable=True, visible=False)
    ops = TemplateColumn(template_name="wall_ops.html",verbose_name=u"操作",orderable=False,attrs={"class":"ops"})
    class Meta:
        model = WallItem
        empty_text = u'暂无微信墙活动'
        order_by = '-id'
        orderable = False
        attrs = {'class' : 'table table-striped'}
        fields = ('event_name', 'keyword', 'begin_time', 'end_time','flag_status' ,'flag_check')
