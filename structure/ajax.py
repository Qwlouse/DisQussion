#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from dajax.core import Dajax

def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()