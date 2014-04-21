# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from framework.forms import RegisterForm
from framework.models import Account, WXAccount
from chartit import DataPool, Chart
from data.models import WeixinDailyData, WSiteDailyData
from datetime import date, timedelta
from microsite.models import App

def get_apps(request):
    account = Account.objects.get(user=request.user)
    wx = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    apps = App.objects.filter(wx=wx)
    return apps

def welcome(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/dashboard')
            else:
                pass
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            account = reg_form.save()

            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)

            return redirect('/')
    else:
        reg_form = RegisterForm()

    return render(request, 'register.html', {'form' : reg_form})

def intro(request):
	if not request.user_agent.is_pc:
	    return redirect("intro/m")
	
	return render(request, "intro.html")

def intro_for_mobile(request):
	return render(request, "intro_m.html")

@login_required
def index(request):
    account = Account.objects.get(user=request.user)
    if account.has_wx_bound:
        return redirect('/dashboard')
    else:
        return redirect('/bind')

@login_required
def bind(request):
	return render(request, 'bind.html')

@login_required
def signout(request):
    logout(request)
    return redirect('/welcome')

@login_required
def account(request):
    account = Account.objects.get(user=request.user)
    group_name = None
    if request.user.groups.count() > 0:
        group_name = request.user.groups.all()[0].name
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]
    return render(request, 'account.html', { 'account' : account, 'group' : group_name, 'wx_account' : wx_account, 'apps' : get_apps(request) })

@login_required
def dashboard(request):
    account = Account.objects.get(user=request.user)
    wx_account = None
    if account.has_wx_bound:
        wx_account = WXAccount.objects.filter(account=account, state=WXAccount.STATE_BOUND)[0]

    if wx_account is not None:
        wsite_ds = DataPool(
            series = [{
            'options' : { 'source' : WSiteDailyData.objects.filter(weixin=wx_account, date__gte=date.today()-timedelta(days=15)).order_by('date')},
            'terms' : ['date_str', 'visitor_count', 'visit_count']
            }])
        wsite_chart = Chart(
            datasource = wsite_ds,
            series_options = [
            { 'options' : {
                'type' : 'line',
                'xAxis' : 0,
                'yAxis' : 0,
                'zIndex' : 1},
            'terms' : {
                'date_str' : ['visitor_count', 'visit_count']
            }}],
            chart_options = {
                'title' : {'text' : u'微官网日访问人数/访问次数'},
                'xAxis' : {'title' : {'text' : u'日期'}},
                'colors' : ['#58ace8', '#f77f74']
           })
        return render(request, 'dashboard.html', {'weixin' : wx_account, 'charts' : [wsite_chart], 'apps' : get_apps(request)})
    else:
        return redirect('/bind')

def agreement(request):
    return render(request, 'agreement.html')

def agreement_game(request):
    return render(request, 'agreement_game.html')
