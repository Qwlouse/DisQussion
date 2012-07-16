#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from structure.models import TextNode, Slot, StructureNode
import json


def getNodeText(node):
    if isinstance(node, TextNode):
        return render_to_string('node/renderTextNode.html',
            {'title' : node.getShortTitle(),
             'text'  : node.getText()})
    elif isinstance(node, Slot):
        return render_to_string('node/renderSlot.html',
            {'title' : node.getShortTitle(),
             'alternatives' : [{'id' : a.nr_in_parent(), 'text' : a.getText()} for a in node.node_set.all()]})
    elif isinstance(node, StructureNode):
        return render_to_string('node/renderStructureNode.html',
            {'title' : node.getShortTitle(),
             'slots' : [{'short_title' : s.getShortTitle(), 'text' : s.getText()} for s in node.slot_set.all()]})
    else :
        return ""

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
    return json.dumps({'text' : getNodeText(node),
                       'type' : node.getType(),
                       'short_title' : node.getShortTitle(),
                       'id' : node.id,
                       'children' : [ {'short_title' : c.getShortTitle(), 'type' : c.getType(), 'id' : c.id} for c in children]
                       })