#!/usr/bin/python
# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import accounts.urls
import settings

# Dajax URLs
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'DisQussion.views.home', name='home'),
    # url(r'^DisQussion/', include('DisQussion.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # User administration
    url(r'^\.users/', include(accounts.urls)),

    # Uncomment the next line to enable the admin:
    url(r'^\.admin/', include(admin.site.urls)),

    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    
    url(r'^(?P<path>([a-zA-Z-_]+\.\d+/)*[a-zA-Z-_]+\.\d+/?)$', 'DisQussion.views.path')
)

# Static files for development
urlpatterns += staticfiles_urlpatterns()
