from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.views',
    url(r'setting/(?P<active_tab_id_id>\d+)', 'setting'),
    url(r'setting', 'setting'),
    url(r'save/(?P<page_id>\d+)', 'save'),
)
