#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from structure.models import TextNode, StructureNode, Slot, Node
from structure.path_helpers import getRootNode

root = getRootNode()
nodeDict = {'root' : root}

def populateNodeDict():
    global nodeDict
    textNodeDict = {t.getTextPath() : t  for t in TextNode.objects.all()}
    structureNodeDict = {sn.getTextPath() : sn  for sn in StructureNode.objects.all()}
    slotDict = {s.getTextPath() : s  for s in Slot.objects.all()}
    nodeDict.update(textNodeDict)
    nodeDict.update(structureNodeDict)
    nodeDict.update(slotDict)


def lookupNode(node, Type=Node):
    if isinstance(node, TextNode) or isinstance(node, StructureNode) or isinstance(node, Slot):
        return node
    if isinstance(node, Node):
        return node.as_leaf_class()
    if isinstance(node, str) or isinstance(node, unicode):
        return nodeDict[node]
    if isinstance(node, int):
        if Type == Node:
            return Node.objects.get(pk=node).as_leaf_class()
        else :
            return Type.objects.get(pk=node)


def createText(parent, text, sources=()):
    global nodeDict
    t = TextNode()
    t.parent = lookupNode(parent, Slot)
    t.text = text
    t.save()
    for s in sources:
        t.sources.add(s)
    t.save()
    nodeDict[t.getTextPath()] = t
    return t

def createSlot(parent, short_title, text=None):
    global nodeDict
    s = Slot()
    s.short_title = short_title
    s.parent = lookupNode(parent, StructureNode)
    s.save()
    nodeDict[s.getTextPath()] = s
    if text is not None:
        return s, createText(s, text)
    else :
        return s

def createStructure(parent, slots):
    global nodeDict
    st = StructureNode()
    st.parent = lookupNode(parent, Slot)
    st.save()
    if isinstance(slots, dict):
        slot_list = [createSlot(st, s, t) for s, t in slots.items()]
    else :
        slot_list = [createSlot(st, s) for s in slots]
    return st, slot_list

