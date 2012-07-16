#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from structure.forms import VotingForm
from structure.models import TextNode, Slot, StructureNode, Vote
import json
from structure.vote_helpers import vote_for_textNode


def getNodeText(node, request):
    if isinstance(node, TextNode):
        #get vote
        votes = Vote.objects.filter(user = request.user, text=node)
        if votes :
            vote = votes[0]
            votingForm = VotingForm(initial={'text_id' : node.id, 'consent' : vote.consent, 'wording' : vote.wording})
        else:
            votingForm = VotingForm(initial={'text_id' : node.id})

        return render_to_string('node/renderTextNode.html',
            {'title' : node.getShortTitle(),
             'text'  : node.getText(),
             'form'  : votingForm})
    elif isinstance(node, Slot):
        return render_to_string('node/renderSlot.html',
            {'title' : node.getShortTitle(),
             'alternatives' : [{'id' : a.nr_in_parent(), 'text' : a.getText()} for a in node.node_set.order_by('-consent_cache')]})
    elif isinstance(node, StructureNode):
        return render_to_string('node/renderStructureNode.html',
            {'title' : node.getShortTitle(),
             'slots' : [{'short_title' : s.getShortTitle(), 'text' : s.getText()} for s in node.slot_set.all()]})
    else :
        return ""

@dajaxice_register
def getNodeInfo(request, node_id, node_type):
    type = {'Slot' : Slot,
            'TextNode' : TextNode,
            'StructureNode' : StructureNode}[node_type]
    node = type.objects.get(pk=node_id)
    children = []
    if isinstance(node, Slot):
        children = [c.as_leaf_class() for c in node.node_set.all()]
    elif isinstance(node, StructureNode):
        children = node.slot_set.all()
    return json.dumps({'text' : getNodeText(node, request),
                       'type' : node.getType(),
                       'short_title' : node.getShortTitle(),
                       'id' : node.id,
                       'children' : [ {'short_title' : c.getShortTitle(), 'type' : c.getType(), 'id' : c.id} for c in children]
                       })


@dajaxice_register
def submitVoteForTextNode(request, text_id, consent, wording):
    user = request.user
    node = TextNode.objects.get(id=text_id)
    vote_for_textNode(user, node, consent, wording)
    return json.dumps(dict())