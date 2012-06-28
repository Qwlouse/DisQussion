#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string

@dajaxice_register
def test(request):
    print("Test wurde aufgerufen.")
    dajax = Dajax()
    dajax.assign('#textPart','innerHTML','<h1>TEST</h1>')
    return dajax.json()

@dajaxice_register
def getNodeText(request, node_id):
    print('#'+node_id)
    dajax = Dajax()
    dajax.assign('#'+node_id, 'textPart', render_to_string('node/renderSlotText.html',
            {'slot_name': "Wahlprogramm", 'alternatives': [
                {'id': "1", 'text':"Ist wichtig"},
                {'id': "2", 'text':"Ist Orange"},
                {'id': "3", 'text':"Ist voll unnötig"}
                ]}))
    return dajax.json()