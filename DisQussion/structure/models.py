#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.db import models

short_title_max_length = 20


class Slot(models.Model):
    parent = models.ForeignKey("StructureNode")
    short_title = models.CharField(max_length=short_title_max_length) #todo: disallow null

class TextNode(models.Model):
    parent = models.ForeignKey(Slot)
    text = models.TextField()

class StructureNode(models.Model):
    parent = models.ForeignKey(Slot, null=True)


