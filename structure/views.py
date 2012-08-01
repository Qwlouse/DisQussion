#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.http import HttpResponseRedirect
from structure.models import TextNode, Slot, Vote

def add_auto_upvote(user, text):
    auto_upvote = Vote()
    auto_upvote.consent = 1
    auto_upvote.wording = 1
    auto_upvote.user = user
    auto_upvote.text = text
    auto_upvote.save()


def submit_textNode(request):
    t = TextNode()
    t.text = request.POST['text']
    t.parent_id = int(request.POST['slot_id'])
    t.save()
    add_auto_upvote(request.user, t)
    return HttpResponseRedirect(t.getTextPath())


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
