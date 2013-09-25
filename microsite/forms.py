#coding:utf8
from django import forms
from django.forms import ModelForm
from models import *
from django.contrib.contenttypes.models import ContentType
from ajax_upload.widgets import AjaxClearableFileInput
from utils import get_wx_access_token

from ckeditor.widgets import CKEditorWidget

class MenuForm(forms.Form):
    app_id = forms.CharField(label=u'AppId', required=True)
    app_secret = forms.CharField(label=u'AppSecret', required=True)

    def clean(self):
        if not self.cleaned_data.has_key('app_id') or self.cleaned_data['app_id'] is None:
            raise forms.ValidationError('AppId不能为空')
        if not self.cleaned_data.has_key('app_secret') or self.cleaned_data['app_secret'] is None:
            raise forms.ValidationError('AppSecret不能为空')

        app_id = self.cleaned_data['app_id']
        app_secret = self.cleaned_data['app_secret']
        
        if app_id and app_secret:
            access_token = get_wx_access_token(app_id, app_secret)
            if access_token is not None:
                self.cleaned_data['access_token'] = access_token
            else:
                raise forms.ValidationError(u'AppId和AppSecret验证失败')

        return self.cleaned_data

class AddEditMenuForm(ModelForm):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Menu
        fields = ('id', 'page', 'name')

class AddEditContactPeopleForm(ModelForm):
    id = forms.CharField(required=False)
    tab_id = forms.CharField()
    class Meta:
        model = ContactPeople
        fields = ('contact_item', 'name', 'email', 'phone', 'qq', 'id', 'tab_id')

class HomePageForm(ModelForm):
    pic1 = forms.ImageField(label=u'焦点图1', widget=AjaxClearableFileInput(), help_text=u"建议焦点图的尺寸相同以保证焦点图的最佳显示效果")
    pic2 = forms.ImageField(label=u'焦点图2', widget=AjaxClearableFileInput(), required = False)
    pic3 = forms.ImageField(label=u'焦点图3', widget=AjaxClearableFileInput(), required = False)
    pic4 = forms.ImageField(label=u'焦点图4', widget=AjaxClearableFileInput(), required = False)
    message_cover = forms.ImageField(label=u'消息封面', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片宽度大于640像素")

    class Meta:
        model = HomePage
        fields = (
            'name',
            'template_type',
            'pic1',
            'pic2',
            'pic3',
            'pic4',
            'exp1',
            'exp2',
            'exp3',
            'exp4',
            'message_cover',
            'message_description',
        )

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(HomePageForm, self).save(commit=False)
        m.wx.wsite_template = m.template_type
        m.wx.save()
        if commit:
            m.save()
        return m

class IntroPageForm(ModelForm):
    content = forms.CharField(label=u'内容', widget=CKEditorWidget())
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px") 
    class Meta:
        model = IntroPage
        fields = (
            'enable',
            'icon',
            'title',
            'content',
        )

class JoinPageForm(ModelForm):
    content = forms.CharField(label=u'内容', widget=CKEditorWidget()) 
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = JoinPage
        fields = (
            'enable',
            'icon',
            'title',
            'content',
        )

class ContactAppForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = ContactApp
        fields = (
            'title',
            'icon',
            'enable',
        )
class TrendsAppForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = TrendsApp
        fields = (
            'title',
            'icon',
            'enable',
        )

class TrendItemForm(ModelForm):
    content = forms.CharField(label=u'内容', widget=CKEditorWidget())
    cover = forms.ImageField(label=u'封面', widget=AjaxClearableFileInput(), required = False, help_text=u'建议图片大小为105px*105px') 
    class Meta:
        model = TrendItem
        fields = (
            'title',
            'content',
            'cover',
            'summary',
        )

class TeamAppForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = TeamApp
        fields = (
            'title',
            'icon',
            'enable',
        )

class TeamItemForm(ModelForm):
    name = forms.CharField(label=u'姓名', widget=forms.TextInput(attrs={'class':'input-xxlarge'}))
    job_title = forms.CharField(label=u'职位名称', widget=forms.TextInput(attrs={'class':'input-xxlarge'}))
    person_digest = forms.CharField(label=u'简要介绍', widget=forms.Textarea(attrs={'class':'input-xxlarge','rows':2}), help_text=u"建议字数限制在50字以内")
    person_content = forms.CharField(label=u'详细介绍', widget=CKEditorWidget())
    picture = forms.ImageField(label=u'照片', widget=AjaxClearableFileInput(), required = True, help_text=u'建议图片大小为105px*105px')
    class Meta:
        model = TeamItem
        fields = (
            'name',
            'job_title',
            'picture',
            'person_digest',
            'person_content',
        )

class ContactItemForm(ModelForm):
    name = forms.CharField(label=u'地址名称', widget=forms.TextInput(attrs={'class':'input-xxlarge'}))
    fax_code = forms.CharField(label=u'传真号码', widget=forms.TextInput(attrs={'class':'input-xxlarge'}), required = False)
    address = forms.CharField(label=u'具体地址', widget=forms.TextInput(attrs={'class':'input-xxlarge'}))
    lat = forms.CharField(widget=forms.HiddenInput())
    lng = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = ContactItem
        fields = (
            'name',
            'fax_code',
            'address',
            'lat',
            'lng',
        )

class ContactPeopleForm(ModelForm):
    class Meta:
        model = ContactPeople
        fields = (
            'contact_item',
            'name',
            'email',
            'phone',
            'qq',
        )

class CulturePageForm(ModelForm):
    content = forms.CharField(label='内容', widget=CKEditorWidget()) 
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = CulturePage 
        fields = (
            'enable',
            'icon',
            'content',
            'title',
        )

class BusinessPageForm(ModelForm):
    content = forms.CharField(label='内容', widget=CKEditorWidget()) 
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = BusinessPage 
        fields = (
            'enable',
            'icon',
            'content',
            'title',
        )

class HelpPageForm(ModelForm):
    content = forms.CharField(label='内容', widget=CKEditorWidget()) 
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = BusinessPage 
        fields = (
            'enable',
            'icon',
            'content',
            'title',
        )


class WeiboPageForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = WeiboPage 
        fields = (
            'enable',
            'icon',
            'title',
            'url',
        )

class ContentPageForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    content = forms.CharField(label=u'内容', widget=CKEditorWidget())
    class Meta:
        model = ContentPage
        fields = (
            'enable',
            'title',
            'icon',
            'content',
        )


class LinkPageForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = LinkPage
        fields = (
            'enable',
            'title',
            'icon',
            'url',
        )

class CaseAppForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = CaseApp
        fields = (
            'title',
            'icon',
            'enable',
        )

class ProductAppForm(ModelForm):
    icon = forms.ImageField(label=u'首页图标', widget=AjaxClearableFileInput(), required = True, help_text=u"建议图片大小为190px*235px")
    class Meta:
        model = ProductApp
        fields = (
            'title',
            'icon',
            'enable',
        )
class CaseItemForm(ModelForm):
    case_pic1 = forms.ImageField(label=u'案例截图1', widget=AjaxClearableFileInput(), required = False, help_text=u"建议焦点图的尺寸相同以保证焦点图的最佳显示效果")
    case_pic2 = forms.ImageField(label=u'案例截图2', widget=AjaxClearableFileInput(), required = False)
    case_pic3 = forms.ImageField(label=u'案例截图3', widget=AjaxClearableFileInput(), required = False)
    case_pic4 = forms.ImageField(label=u'案例截图4', widget=AjaxClearableFileInput(), required = False)
    case_intro = forms.CharField(label=u'内容', widget=CKEditorWidget())
    class Meta:
        model = CaseItem
        fields = (
            'title',
            'cls',
            'case_pic1',
            'case_pic2',
            'case_pic3',
            'case_pic4',
            'case_intro',
        )

class CaseClassForm(ModelForm):
    class Meta:
        model = CaseClass
        fields = (
            'name',
        )
        

class ProductItemForm(ModelForm):
    product_pic1 = forms.ImageField(label=u'产品截图1', widget=AjaxClearableFileInput(), required = False, help_text=u"建议焦点图的尺寸相同以保证焦点图的最佳显示效果")
    product_pic2 = forms.ImageField(label=u'产品截图2', widget=AjaxClearableFileInput(), required = False)
    product_pic3 = forms.ImageField(label=u'产品截图3', widget=AjaxClearableFileInput(), required = False)
    product_pic4 = forms.ImageField(label=u'产品截图4', widget=AjaxClearableFileInput(), required = False)
    product_intro = forms.CharField(label=u'内容', widget=CKEditorWidget())
    class Meta:
        model = ProductItem
        fields = (
            'title',
            'cls',
            'product_pic1',
            'product_pic2',
            'product_pic3',
            'product_pic4',
            'product_intro',
        )

class ProductClassForm(ModelForm):
    class Meta:
        model = ProductClass
        fields = (
            'name',
        )

class AddCaseClassForm(forms.Form):
    name = forms.CharField()
    tab_id = forms.IntegerField()

    def clean_name(self):
        try:
            CaseClass.objects.get(name=self.cleaned_data['name'])
        except CaseClass.DoesNotExist:
            return self.cleaned_data['name']

        raise forms.ValidationError(u'分类已经存在！')

class AddProductClassForm(forms.Form):
    name = forms.CharField()
    tab_id = forms.IntegerField()

    def clean_name(self):
        try:
            ProductClass.objects.get(name=self.cleaned_data['name'])
        except ProductClass.DoesNotExist:
            return self.cleaned_data['name']

        raise forms.ValidationError(u'分类已经存在！')

class ChangeCaseClassForm(forms.Form):
    name_change = forms.CharField()
    tab_id_change = forms.IntegerField()
    record_id_change = forms.IntegerField()

    def clean_name_change(self):
        try:
            CaseClass.objects.get(name=self.cleaned_data['name_change'])
        except CaseClass.DoesNotExist:
            return self.cleaned_data['name_change']

        raise forms.ValidationError(u'分类已经存在！')

class ChangeProductClassForm(forms.Form):
    name_change = forms.CharField()
    tab_id_change = forms.IntegerField()
    record_id_change = forms.IntegerField()

    def clean_name_change(self):
        try:
            ProductClass.objects.get(name=self.cleaned_data['name_change'])
        except ProductClass.DoesNotExist:
            return self.cleaned_data['name_change']

        raise forms.ValidationError(u'分类已经存在！')

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
        elif page.real_type == ContentType.objects.get_for_model(HelpPage):
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
        elif page.real_type == ContentType.objects.get_for_model(TeamApp):
            if (request):
                return TeamAppForm(request.POST, request.FILES, instance=page)
            else:
                return TeamAppForm(instance=page)



