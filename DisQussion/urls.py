#!/usr/bin/python
# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'DisQussion.views.home', name='home'),
    # url(r'^DisQussion/', include('DisQussion.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Login and Logout
    (r'^login$', 'django.contrib.auth.views.login', {'redirect_field_name': "login_redirect"}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'redirect_field_name': "logout_redirect"}),

    # Profiles
    url(r'^profile/', 'DisQussion.views.show_profile'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^(?P<path>([a-zA-Z-_]+\.\d+/)*[a-zA-Z-_]+\.\d+/?)$', 'DisQussion.views.path')
)

# Static files for development
urlpatterns += staticfiles_urlpatterns()
