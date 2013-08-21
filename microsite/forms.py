#coding:utf8
from django import forms
from django.forms import ModelForm
from models import *
from django.contrib.contenttypes.models import ContentType
from ajax_upload.widgets import AjaxClearableFileInput

from ckeditor.widgets import CKEditorWidget



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
    content = forms.CharField(widget=CKEditorWidget()) 
    class Meta:
        model = IntroPage
        fields = (
            'enable',
            'title',
            'content'
        )

class JoinPageForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget()) 
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
    content = forms.CharField(widget=CKEditorWidget()) 
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
    content = forms.CharField(widget=CKEditorWidget()) 
    class Meta:
        model = CulturePage 
        fields = (
            'enable',
            'content',
            'title',
        )

class BusinessPageForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget()) 
    class Meta:
        model = BusinessPage 
        fields = (
            'enable',
            'content',
            'title',
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
    content = forms.CharField(widget=CKEditorWidget()) 
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

class CaseAppForm(ModelForm):
    class Meta:
        model = CaseApp
        fields = (
            'enable',
        )

class ProductAppForm(ModelForm):
    class Meta:
        model = ProductApp
        fields = (
            'enable',
        )
class CaseItemForm(ModelForm):
    case_pic1 = forms.ImageField(label=u'案例截图1', widget=AjaxClearableFileInput(), required = False)
    case_pic2 = forms.ImageField(label=u'案例截图2', widget=AjaxClearableFileInput(), required = False)
    case_pic3 = forms.ImageField(label=u'案例截图3', widget=AjaxClearableFileInput(), required = False)
    case_pic4 = forms.ImageField(label=u'案例截图4', widget=AjaxClearableFileInput(), required = False)
    case_intro = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = CaseItem
        fields = (
            'title',
            'cls',
        )

class ProductClassForm(ModelForm):
    class Meta:
        model = ProductClass
        fields = (
            'name',
        )

class ProductItemForm(ModelForm):
    product_pic1 = forms.ImageField(label=u'产品截图1', widget=AjaxClearableFileInput(), required = False)
    product_pic2 = forms.ImageField(label=u'产品截图2', widget=AjaxClearableFileInput(), required = False)
    product_pic3 = forms.ImageField(label=u'产品截图3', widget=AjaxClearableFileInput(), required = False)
    product_pic4 = forms.ImageField(label=u'产品截图4', widget=AjaxClearableFileInput(), required = False)
    product_intro = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = ProductItem
        fields = (
            'title',
            'cls',
        )

class ProductClassForm(ModelForm):
    class Meta:
        model = ProductClass
        fields = (
            'name',
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
        elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
            if (request):
                return BusinessPageForm(request.POST, request.FILES, instance=page)
            else:
                return BusinessPageForm(instance=page)
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
        elif page.real_type == ContentType.objects.get_for_model(CaseApp):
            if (request):
                return CaseAppForm(request.POST, request.FILES, instance=page)
            else:
                return CaseAppForm(instance=page)
        elif page.real_type == ContentType.objects.get_for_model(ProductApp):
            if (request):
                return ProductAppForm(request.POST, request.FILES, instance=page)
            else:
                return ProductAppForm(instance=page)






