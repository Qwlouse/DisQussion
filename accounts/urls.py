#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Login and Logout
    (r'^login$', 'django.contrib.auth.views.login', {'redirect_field_name': "login_redirect"}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'redirect_field_name': "logout_redirect"}),

    # Profiles
    url(r'^(?P<user_name>(\w+))', 'accounts.views.show_profile'),
)