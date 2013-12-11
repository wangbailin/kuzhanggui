from django.conf.urls.defaults import *

urlpatterns = patterns('wall.views',
    url(r'^weixinwall', 'wall'),
    url(r'^wall/(?P<item_id>\d+)/delete', 'wall_delete'),
    url(r'^wall/(?P<item_id>\d+)/show', 'wall_show'),
    url(r'^wall/(?P<item_id>\d+)/conduct', 'wall_conduct'),
)
