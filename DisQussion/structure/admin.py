#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from models import StructureNode, TextNode, Slot
from django.contrib import admin

admin.site.register(StructureNode)
admin.site.register(TextNode)
admin.site.register(Slot)

