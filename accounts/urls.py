#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.conf.urls import patterns, include, url

from django.contrib.auth.views import password_change

urlpatterns = patterns('',
    # Login and Logout
    (r'^login$', 'django.contrib.auth.views.login', {'redirect_field_name': "login_redirect"}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'redirect_field_name': "logout_redirect"}),

    # Change User info
    (r'^change_email$', 'accounts.views.change_email'),
    (r'^change_password/(?P<post_change_redirect>([\w./]+))$', 'django.contrib.auth.views.password_change'), # FIXME: Fieser HACK
    (r'^change_description$', 'accounts.views.change_description'),
    # Profiles
    url(r'^(?P<user_name>(\w+))', 'accounts.views.show_profile'),
)