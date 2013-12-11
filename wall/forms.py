#coding:utf8
from django import forms
from django.forms import ModelForm, Textarea
from models import *
from django.contrib.contenttypes.models import ContentType
from ajax_upload.widgets import AjaxClearableFileInput
from datetimewidget.widgets import DateTimeWidget
from datetime import datetime
from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

class HorizRadioRenderer(RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class WallItemForm(ModelForm):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    event_name = forms.CharField(label=u'活动名称', max_length=20, required=True, help_text=u'20字以内')
    keyword = forms.CharField(label=u'关键字', max_length=10, required=True, help_text=u'10字以内')
    begin_time = forms.DateTimeField(label=u"活动起始时间", required=True, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'format' : 'mm/dd/yyyy HH:ii P',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    end_time = forms.DateTimeField(label=u"活动结束时间", required=True, widget=DateTimeWidget(options={
                'autoclose' : 'true',
                'format' : 'mm/dd/yyyy HH:ii P',
                'showMeridian' : 'true',
                'startDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }))
    RADIO_CHOICES = ( ('是', u'需要审核'), ('否', u'无需审核'))
    flag_check = forms.ChoiceField(label=u'是否审核', widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=RADIO_CHOICES, initial='是')
    welcome = forms.CharField(label=u'欢迎语', required=True, widget=Textarea(attrs={'rows': '2', 'class':'input-medium'})) 
    RADIO_CHOICES2 = (('是',u'显示昵称'),('否',u'显示匿名'))
    anonymity = forms.ChoiceField(label=u'是否匿名', widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=RADIO_CHOICES2, initial='是')
    class Meta:
        model = WallItem
        fields = (
            'id',
            'event_name',
            'keyword',
            'welcome',
            'begin_time',
            'end_time',
            'flag_check',
            'anonymity'
        )

