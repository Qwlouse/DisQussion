#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from structure.models import TextNode, Slot, Vote
from structure.forms import CreateTextNodeForm
from structure.ajax import getNavigationData, getDataForAlternativesGraph
from structure_parser import  parse
def add_auto_upvote(user, text):
    auto_upvote = Vote()
    auto_upvote.consent = 1
    auto_upvote.wording = 1
    auto_upvote.user = user
    auto_upvote.text = text
    auto_upvote.save()


def submit_textNode(request):
    text = request.POST['text']
    parent_id = int(request.POST['slot_id'])
    slot = Slot.objects.get(id=parent_id)
    new_node = parse(text, slot)
    #TODO: add_auto_upvote(request.user, t)
    return HttpResponseRedirect(new_node.getTextPath())


def submit_slot_with_text(request):
    short_title = request.POST['short_title']
    if not  short_title:
        return "ERROR: Short Title darf nicht leer sein."
    parent_id = int(request.POST['parent_id'])
    # lookup if slot exists
    slots = Slot.objects.filter(parent__id=parent_id, short_title=short_title)
    if slots:
        s = slots[0]
    else :
        s = Slot()
        s.short_title = request.POST['short_title']
        s.parent_id = parent_id
        s.save()

    t = TextNode()
    t.text = request.POST['text']
    t.parent = s
    t.save()
    add_auto_upvote(request.user, t)
    return HttpResponseRedirect(t.getTextPath())


def refine_node(request, id):
    pattern_node = TextNode.objects.get(pk=id)
    createTextNodeForm = CreateTextNodeForm({'text' : pattern_node.getText(), 'slot_id' : pattern_node.parent_id})
    anchor_nodes = getDataForAlternativesGraph(request, pattern_node.parent_id)
    return render_to_response("node/refine.html",
            {"pagename": "Verbessern oder erweitern von "+pattern_node.getShortTitle(),
             "pattern_title": pattern_node.getShortTitle(),
             "pattern_text": pattern_node.getText(),
             "this_url": pattern_node.getTextPath(),
             "authForm": AuthenticationForm(),
             "navigation" : getNavigationData(request, pattern_node.id, pattern_node.getType()),
             "anchor_nodes" : anchor_nodes,
             "selected_id" : pattern_node.id,
             "parent_id" : pattern_node.parent_id,
             "refine_form" : createTextNodeForm
             },
        context_instance=RequestContext(request))


def create_node(request, parent_id):
    parent = Slot.objects.get(pk=parent_id)
    createTextNodeForm = CreateTextNodeForm({'text' : "", 'slot_id' : parent_id})
    anchor_nodes = getDataForAlternativesGraph(request, parent.id)
    return render_to_response("node/create.html",
            {"pagename": "Alternative erstellen in "+parent.getShortTitle(),
             "slot_title": parent.getShortTitle(),
             "authForm": AuthenticationForm(),
             "navigation" : getNavigationData(request, parent_id, parent.getType()),
             "anchor_nodes" : anchor_nodes,
             "alternative_form" : createTextNodeForm
            },
        context_instance=RequestContext(request))