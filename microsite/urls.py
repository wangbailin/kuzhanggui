from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.views',
    url(r'^settings/(?P<active_tab_id>\d+)', 'settings'),
    url(r'^settings', 'settings'),
    url(r'^save/(?P<page_id>\d+)', 'save'),
    url(r'^app/(?P<app_id>\d+)', 'app'),
    url(r'^contact/add', 'add_edit_contact'),
    url(r'^contact/(?P<item_id>\d+)/edit', 'add_edit_contact'),
    url(r'^contact/(?P<item_id>\d+)/delete', 'contact_delete'),
    url(r'^contact_people/add', 'add_edit_contact_people'),
    url(r'^contact_people/(?P<item_id>\d+)/edit', 'add_edit_contact_people'),
    url(r'^contact_people/(?P<item_id>\d+)/delete', 'contact_people_delete'),
    url(r'^trend/add', 'add_edit_trend'),
    url(r'^trend/(?P<item_id>\d+)/edit', 'add_edit_trend'),
    url(r'^trend/(?P<item_id>\d+)/delete', 'trend_delete'),
    url(r'^case/add', 'add_edit_case'),
    url(r'^case/(?P<item_id>\d+)/edit', 'add_edit_case'),
    url(r'^case/(?P<item_id>\d+)/delete', 'case_delete'),
    url(r'^case_class/add', 'add_edit_case_class'),
    url(r'^case_class/(?P<item_id>\d+)/edit', 'add_edit_case_class'),
    url(r'^case_class/(?P<item_id>\d+)/delete', 'case_class_delete'),
    url(r'^product/add', 'add_edit_product'),
    url(r'^product/(?P<item_id>\d+)/edit', 'add_edit_product'),
    url(r'^product/(?P<item_id>\d+)/delete', 'product_delete'),
    url(r'^product_class/add', 'add_edit_product_class'),
    url(r'^product_class/(?P<item_id>\d+)/edit', 'add_edit_product_class'),
    url(r'^product_class/(?P<item_id>\d+)/delete', 'product_class_delete'),
    url(r'^link_page/add', 'add_edit_link_page'),
    url(r'^content_page/add', 'add_edit_content_page'),
)
