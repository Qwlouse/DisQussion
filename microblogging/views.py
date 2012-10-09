#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from django.http import HttpResponseRedirect
import time
from microblogging.models import Entry

def submit_Microblog_Entry(request):
    p = Entry()
    p.content = request.POST['text']
    p.user = request.user
    p.save()
    return HttpResponseRedirect(request.POST['post_redirect'])