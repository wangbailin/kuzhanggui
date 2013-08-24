from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse
def homepage(request, item_id):
    return HttpResponse("not ok now")
