from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.preview',
    url(r'page/(?P<page_id>\d+)', 'page'),
)
