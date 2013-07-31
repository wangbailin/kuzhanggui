#coding:utf8
from django import forms
from django.forms import ModelForm
from models import *
from django.contrib.contenttypes.models import ContentType
from ajax_upload.widgets import AjaxClearableFileInput




class HomePageForm(ModelForm):
    pic1 = forms.ImageField(label=u'焦点图1', widget=AjaxClearableFileInput(), required = False)
    pic2 = forms.ImageField(label=u'焦点图2', widget=AjaxClearableFileInput(), required = False)
    pic3 = forms.ImageField(label=u'焦点图3', widget=AjaxClearableFileInput(), required = False)
    pic4 = forms.ImageField(label=u'焦点图4', widget=AjaxClearableFileInput(), required = False)
    class Meta:
        model = HomePage
        fields = (
            'name',
            'template_type',
            'pic1',
            'pic2',
            'pic3',
            'pic4',
            'cover',
            'content',
        )

class IntroPageForm(ModelForm):
    class Meta:
        model = IntroPage
        fields = (
            'enable',
            'title',
            'content'
        )

class JoinPageForm(ModelForm):
    class Meta:
        model = JoinPage
        fields = (
            'enable',
            'title',
            'content'
        )

class ContactAppForm(ModelForm):
    class Meta:
        model = ContactApp
        fields = (
            'enable',
        )
class TrendsAppForm(ModelForm):
    class Meta:
        model = TrendsApp
        fields = (
            'enable',
        )

class TrendItemForm(ModelForm):
    class Meta:
        model = TrendItem
        fields = (
            'title',
            'content',
        )

class ContactItemForm(ModelForm):
    class Meta:
        model = ContactItem
        fields = (
            'name',
            'address',
            'mail_code',
            'fax_code',
        )

class ContactPeopleForm(ModelForm):
    class Meta:
        model = ContactPeople
        fields = (
            'name',
            'email',
            'phone',
            'qq',
        )

class CulturePageForm(ModelForm):
    class Meta:
        model = CulturePage 
        fields = (
            'enable',
            'title',
            'content',
        )

class WeiboPageForm(ModelForm):
    class Meta:
        model = WeiboPage 
        fields = (
            'enable',
            'title',
            'url',
        )

class ContentPageForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput())
    class Meta:
        model = ContentPage
        fields = (
            'enable',
            'title',
            'icon',
            'content',
        )


class LinkPageForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput())
    class Meta:
        model = LinkPage
        fields = (
            'enable',
            'title',
            'icon',
            'url',
        )

class FormManager(object):
    @classmethod
    def get_form(cls, page, request = None):
        if page.real_type == ContentType.objects.get_for_model(HomePage):
            if (request):
                return HomePageForm(request.POST, request.FILES, instance=page)
            else:
                return HomePageForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(IntroPage):
            if (request):
                return IntroPageForm(request.POST, request.FILES, instance=page)
            else:
                return IntroPageForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(JoinPage):
            if (request):
                return JoinPageForm(request.POST, request.FILES, instance=page)
            else:
                return JoinPageForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(ContactApp):
            if (request):
                return ContactAppForm(request.POST, request.FILES, instance=page)
            else:
                return ContactAppForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
            if (request):
                return TrendsAppForm(request.POST, request.FILES, instance=page)
            else:
                return TrendsAppForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(CulturePage):
            if (request):
                return CulturePageForm(request.POST, request.FILES, instance=page)
            else:
                return CulturePageForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
            if (request):
                return WeiboPageForm(request.POST, request.FILES, instance=page)
            else:
                return WeiboPageForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(ContentPage):
            if (request):
                return ContentPageForm(request.POST, request.FILES, instance=page)
            else:
                return ContentPageForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(LinkPage):
            if (request):
                return LinkPageForm(request.POST, request.FILES, instance=page)
            else:
                return LinkPageForm(instance=page)



