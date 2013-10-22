# coding:utf-8

from django import template
from django.contrib.contenttypes.models import ContentType

from microsite.models import PageGroup

register = template.Library()

@register.filter
def menu_pages(menu):
    pages = PageGroup.objects.filter(menu=menu)
    return ','.join([str(p.page.pk) for p in pages])

@register.filter
def menu_page_names(menu):
    items = PageGroup.objects.filter(menu=menu).order_by("position")
    return ', '.join([item.page.tab_name for item in items]) if len(items) != 0 else u'－'

