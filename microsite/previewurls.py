from django.conf.urls.defaults import *

urlpatterns = patterns('microsite.preview',
    url(r'page/(?P<page_id>\d+)', 'page'),
    url(r'join_item$', 'join_item'),
    url(r'trend_item$', 'trend_item'),
    url(r'team_item$', 'team_item'),
    url(r'case_item$', 'case_item'),
    url(r'case_item/(?P<item_id>\d+)', 'case_item'),
    url(r'product_item$', 'product_item'),
    url(r'product_item/(?P<item_id>\d+)', 'product_item'),
    url(r'content_page', 'content'),
    url(r'link_page', 'link'),
)
