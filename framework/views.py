# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from framework.forms import RegisterForm
from framework.models import Account, WXAccount

def welcome(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
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

@login_required
def index(request):
    account = Account.objects.get(user=request.user)
    if account.has_wx_bound:
        return render(request, 'framework.html')
    else:
        return redirect('/bind')

@login_required
def bind(request):
	return render(request, 'bind.html')

@login_required
def signout(request):
    logout(request)
    return redirect('/welcome')

def agreement(request):
    return render(request, 'agreement.html')

def agreement_game(request):
    return render(request, 'agreement_game.html')