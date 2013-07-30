from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.views',
    url(r'^setting/(?P<active_tab_id_id>\d+)', 'setting'),
    url(r'^setting', 'setting'),
    url(r'^save/(?P<page_id>\d+)', 'save'),
    url(r'^app/(?P<app_id>\d+)', 'app'),
    url(r'^contact/add', 'add_edit_contact'),
    url(r'^contact/(?P<item_id>\d+)/edit', 'add_edit_contact'),
    url(r'^trend/add', 'add_edit_trend'),
    url(r'^trend/(?P<item_id>\d+)/edit', 'add_edit_trend'),
    url(r'^contact_people/(?P<contact_id>\d+)/add', 'add_edit_contact_people'),
    url(r'^contact_people/(?P<contact_id>\d+)/(?P<item_id>\d+)/edit', 'add_edit_contact_people'),
    url(r'^link_page/add', 'add_edit_link_page'),
    url(r'^content_page/add', 'add_edit_content_page'),
)
