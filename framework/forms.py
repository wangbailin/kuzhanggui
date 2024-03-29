# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.core.cache import cache
import datetime

from models import Account

class RegisterForm(forms.Form):
    username = forms.RegexField(min_length=6, max_length=18, required=True, regex='^[a-zA-Z0-9]\w+')
    password1 = forms.CharField(min_length=6, max_length=16, required=True, widget=forms.widgets.PasswordInput())
    password2 = forms.CharField(min_length=6, max_length=16, required=True, widget=forms.widgets.PasswordInput())
    phone = forms.RegexField(min_length=11, max_length=11, required=True, regex='^1\d+')
    auth_code = forms.RegexField(min_length=6, max_length=6, required=True, regex='\d+')
    email = forms.EmailField(required=False)
    qq = forms.RegexField(min_length=6, max_length=20, required=False, regex='\d+')

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        
        raise forms.ValidationError(u'用户名已存在，请尝试其他用户名')

    def clean_auth_code(self):
        auth_code = cache.get('auth_code_' + self.cleaned_data['phone'])
        if auth_code != self.cleaned_data['auth_code']:
            raise forms.ValidationError(u'验证码错误')

        return self.cleaned_data['auth_code']

    def clean_password2(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'两次输入的密码不一致')

        return self.cleaned_data['password2']

    def save(self):
        new_user = User.objects.create_user(username = self.cleaned_data['username'],
            password = self.cleaned_data['password1'],
            email = self.cleaned_data['email'])
        new_account = Account.objects.create(user=new_user, 
            phone=self.cleaned_data['phone'], 
            qq=self.cleaned_data['qq'],
            expired_time=datetime.datetime.now() + datetime.timedelta(weeks=8))

        # add new account as trial account
        new_account.user.groups = Group.objects.filter(name=u'试用账户')

        return new_account

class ChangePasswordForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=18, required=True)
    password_old = forms.CharField(min_length=6, max_length=16, required=True, widget=forms.widgets.PasswordInput())
    password_new1 = forms.CharField(min_length=6, max_length=16, required=True, widget=forms.widgets.PasswordInput())
    password_new2 = forms.CharField(min_length=6, max_length=16, required=True, widget=forms.widgets.PasswordInput())

    def clean_password_old(self):
        if 'username' in self.cleaned_data and 'password_old' in self.cleaned_data:
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password_old'])
            if user is None or not user.is_active:
                raise forms.ValidationError(u'密码不正确')

        return self.cleaned_data['password_old']

    def clean_password_new2(self):
        if 'password_new1' in self.cleaned_data and 'password_new2' in self.cleaned_data:
            if self.cleaned_data['password_new1'] != self.cleaned_data['password_new2']:
                raise forms.ValidationError(u'两次输入的密码不一致')

        return self.cleaned_data['password_new2']

    def save(self):
        user = User.objects.get(username__exact=self.cleaned_data['username'])
        user.set_password(self.cleaned_data['password_new1'])
        user.save()

class EditAccountForm(forms.Form):
    email = forms.EmailField(required=False)
    qq = forms.RegexField(min_length=6, max_length=20, required=False, regex='\d+')

class ChangePhoneForm(forms.Form):
    phone = forms.RegexField(min_length=11, max_length=11, required=True, regex='^1\d+')
    auth_code = forms.RegexField(min_length=6, max_length=6, required=True, regex='\d+')

    def clean_auth_code(self):
        auth_code = cache.get('auth_code_' + self.cleaned_data['phone'])
        if auth_code != self.cleaned_data['auth_code']:
            raise forms.ValidationError(u'验证码错误')

