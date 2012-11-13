#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from django.http import HttpResponseRedirect
from microblogging.models import create_entry

def submit_Microblog_Entry(request):
    p = create_entry(request.POST['text'], request.user)
    return HttpResponseRedirect(request.POST['post_redirect'])