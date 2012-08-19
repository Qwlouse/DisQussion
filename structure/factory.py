#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.contrib.auth.models import User
from structure.models import TextNode, StructureNode, Slot, Node, Vote, adjust_vote_caches
from structure.path_helpers import getRootNode
from structure.vote_helpers import vote_for_textNode


nodeDict = dict()

def populateNodeDict():
    global nodeDict
    root = getRootNode()
    nodeDict['root'] = root
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

def createDummyUsers(cnt):
    dummy_users_count = User.objects.filter(username__startswith="user_").count()
    new_users = []
    for i in range(dummy_users_count, dummy_users_count+cnt):
        name = "user_" + str(i)
        new_users.append(User.objects.create_user(name, name + "@server", "password"))
    return new_users


def castVotesFor(text, consent):
    dummy_users = User.objects.filter(username__startswith="user_")
    # get/create users that can cast additional votes
    free_users = list(dummy_users.exclude(vote__text=text))
    number_of_votes = sum(consent)
    number_of_free_users = len(free_users)
    if number_of_free_users < number_of_votes :
        additional_users = createDummyUsers(number_of_votes - number_of_free_users)
        free_users += additional_users

    # generate the votes
    consent_values = [-1] * consent[0]  + [1] * consent[1]
    for i in range(number_of_votes):
        vote_for_textNode(free_users[i], text, consent_values[i])

def clearVotesFor(text):
    Vote.objects.filter(text=text).delete()
    adjust_vote_caches(text)
