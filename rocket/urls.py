from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import settings
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'', include('framework.urls')),
    url(r'', include('microsite.urls')),
    #url(r'', include('wall.urls')),
    url(r'^wx/', include('weixin.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^ajax-upload/', include('ajax_upload.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    #url(r'^select2/', include('django_select2.urls')),
    url(r'^api/microsite/', include('microsite.apiurls')),
    url(r'^microsite/', include('microsite.siteurls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

