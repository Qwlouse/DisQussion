#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.contrib import admin
from models import Entry

admin.site.register(Entry)