import logging
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse
from models import *
logger = logging.getLogger('default')
def homepage(request, item_id):
    homepage = get_object_or_404(HomePage, pk=item_id)
    pics = []
    if homepage.pic1:
        pics.append(homepage.pic1)
    if homepage.pic2:
        pics.append(homepage.pic2)
    if homepage.pic3:
        pics.append(homepage.pic3)
    if homepage.pic4:
        pics.append(homepage.pic4)
    logger.debug("%s" % str(pics))
    return render(request, 'microsite/homepage.html', {'name':homepage.name, 'pics':pics})
