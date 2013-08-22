from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.apiviews',
    url(r'homepage/(?P<item_id>\d+)', 'homepage'),
    #url(r'intropage/(?P<item_id>\d+)', 'intropage'),
    #url(r'business/(?P<item_id>\d+)', 'business'),
    #url(r'trend/(?P<item_id>\d+)', 'trend'),
    #url(r'joinus/(?P<item_id>\d+)', 'joinus'),
    #url(r'contact/(?P<item_id>\d+)', 'contact'),
    #url(r'case/(?P<item_id>\d+)', 'case'),
    #url(r'product/(?P<item_id>\d+)', 'product'),
    #url(r'weibo/(?P<item_id>\d+)', 'weibo'),
)
