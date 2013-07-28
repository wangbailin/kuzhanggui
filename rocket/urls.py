from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('framework.urls')),
    url(r'', include('microsite.urls')),
    url(r'^ajax-upload/', include('ajax_upload.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

