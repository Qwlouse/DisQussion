#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.http import HttpResponseRedirect
from structure.models import TextNode

def submit_textNode(request):
    t = TextNode()
    t.text = request.POST['text']
    t.parent_id = int(request.POST['slot_id'])
    t.save()
    return HttpResponseRedirect("/" + t.getTextPath())
