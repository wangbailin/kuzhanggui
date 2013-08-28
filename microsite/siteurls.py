from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.siteviews',
    url(r'homepage/(?P<item_id>\d+)', 'homepage'),
    url(r'intro/(?P<item_id>\d+)', 'intro'),
    url(r'business/(?P<item_id>\d+)', 'business'),
    url(r'trend/(?P<item_id>\d+)', 'trend'),
    url(r'trenditem/(?P<item_id>\d+)', 'trenditem'),
    url(r'join/(?P<item_id>\d+)', 'join'),
    url(r'weibo/(?P<item_id>\d+)', 'weibo'),
    url(r'case/(?P<item_id>\d+)', 'case'),
    url(r'caseitem/(?P<item_id>\d+)', 'caseitem'),
    url(r'contact/(?P<item_id>\d+)', 'contact'),
    url(r'product/(?P<item_id>\d+)', 'product'),
    url(r'product_item/(?P<item_id>\d+)', 'product_item'),
    url(r'link/(?P<item_id>\d+)', 'link'),
    url(r'content/(?P<item_id>\d+)', 'content'),
)