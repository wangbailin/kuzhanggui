# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render, redirect

def index(request):
	return render(request, "framework.html")

def bind(request):
	return render(request, "bind.html")