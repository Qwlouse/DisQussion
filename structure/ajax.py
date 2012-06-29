#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from structure.models import Node, TextNode, Slot, StructureNode
import json


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

@dajaxice_register
def getNodeInfo(request, node_id, node_type):
    print("getNodeInfo", node_id, node_type)
    type = {'Slot' : Slot,
            'TextNode' : TextNode,
            'StructureNode' : StructureNode}[node_type]
    node = type.objects.get(pk=node_id)
    children = []
    if isinstance(node, Slot):
        children = [c.as_leaf_class() for c in node.node_set.all()]
    elif isinstance(node, StructureNode):
        children = node.slot_set.all()
    return json.dumps({'text' : node.getText(),
                       'type' : node.getType(),
                       'short_title' : node.getShortTitle(),
                       'children' : [ {'short_title' : c.getShortTitle(), 'type' : c.getType(), 'id' : c.id} for c in children]
                       })