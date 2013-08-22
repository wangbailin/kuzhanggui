from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.siteviews',
    url(r'homepage/(?P<item_id>\d+)', 'homepage'),
)
