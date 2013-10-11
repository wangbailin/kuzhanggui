from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('framework.views',
	url(r'^intro$', 'intro'),
	url(r'^intro/m$', 'intro_for_mobile'),
    url(r'^$', 'index'),
    url(r'^welcome', 'welcome'),
    url(r'^bind', 'bind'),
    url(r'^register', 'register'),
    url(r'^signout', 'signout'),
    url(r'^agreement_game', 'agreement_game'),
    url(r'^agreement', 'agreement'),
    url(r'^account', 'account'),
    url(r'^dashboard', 'dashboard')
)
