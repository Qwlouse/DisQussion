#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from dajaxice.decorators import dajaxice_register
from django.template.context import RequestContext
from django.template.loader import render_to_string
from structure.forms import VotingForm, CreateTextNodeForm, CreateSlotWithTextForm
from structure.models import TextNode, Slot, StructureNode, Vote
import json
from structure.path_helpers import getRootNode
from structure.vote_helpers import vote_for_textNode


def getNodeText(node, request):
    if isinstance(node, TextNode):
        #get vote
        votingForm = VotingForm(initial={'text_id' : node.id})
        if request.user.is_authenticated() :
            votes = Vote.objects.filter(user = request.user, text=node)
            if votes :
                vote = votes[0]
                votingForm = VotingForm(initial={'text_id' : node.id, 'consent' : vote.consent, 'wording' : vote.wording})

        return render_to_string('node/renderTextNode.html',
            {'title' : node.getShortTitle(),
             'text'  : node.getText(),
             'consent_rating' : node.calculate_consent_rating(),
             'wording_rating' : node.calculate_wording_rating(),
             'form'  : votingForm},
            RequestContext(request))

    elif isinstance(node, Slot):
        createTextNodeForm = CreateTextNodeForm({'slot_id' : node.id})
        return render_to_string('node/renderSlot.html',
            {'title' : node.getShortTitle(),
             'alternatives' : [{'id' : a.nr_in_parent(),
                                'text' : a.getText(),
                                'consent_rating' : a.calculate_consent_rating(),
                                'wording_rating' : a.calculate_wording_rating()
                                } for a in node.node_set.order_by('-rating')],
             'new_alternative_form' : createTextNodeForm},
            RequestContext(request))

    elif isinstance(node, StructureNode):
        createSlotWithTextForm = CreateSlotWithTextForm({'parent_id' : node.id})

        return render_to_string('node/renderStructureNode.html',
            {'title' : node.getShortTitle(),
             'consent_rating' : node.calculate_consent_rating(),
             'wording_rating' : node.calculate_wording_rating(),
             'slots' : [{'short_title' : s.getShortTitle(), 'text' : s.getText()} for s in node.slot_set.all()],
             'create_slot_with_text_form' : createSlotWithTextForm},
            RequestContext(request))
    else :
        return ""

def getNode(node_id, node_type):
    NodeType = {'Slot' : Slot,
                'TextNode' : TextNode,
                'StructureNode' : StructureNode}[node_type]
    return NodeType.objects.get(pk=node_id)

@dajaxice_register
def getNodeInfo(request, node_id, node_type):
    node = getNode(node_id, node_type)
    children = []
    if isinstance(node, Slot):
        children = [c.as_leaf_class() for c in node.node_set.all()]
    elif isinstance(node, StructureNode):
        children = node.slot_set.all()
    if node.parent is None:
        parent_title = ""
        parent_id = -1
        parent_type = ""
    else :
        parent_title = node.parent.getShortTitle()
        parent_id = node.parent_id
        parent_type = node.parent.getType()
    return json.dumps({'text' : getNodeText(node, request),
                       'type' : node.getType(),
                       'short_title' : node.getShortTitle(),
                       'id' : node.id,
                       'children' : [ {'short_title' : c.getShortTitle(), 'type' : c.getType(), 'id' : c.id} for c in children],
                       'parent' : {'short_title' : parent_title, 'type' : parent_type, 'id' : parent_id},
                       'url' : node.getTextPath()
                       })


@dajaxice_register
def submitVoteForTextNode(request, text_id, consent, wording):
    user = request.user
    node = TextNode.objects.get(id=text_id)
    vote_for_textNode(user, node, consent, wording)
    return json.dumps(dict())


def createSlotList(structure_node, selected_slot, selected_alternative):
    slot_list = structure_node.slot_set.order_by("pk")
    return [{'title' : s.getShortTitle() if s != selected_slot else selected_alternative.getShortTitle(),
             'id' : s.pk,
             'path' :  s.getTextPath() if s != selected_slot else selected_alternative.getTextPath(),
             'selected' : s == selected_slot} for s in slot_list]

@dajaxice_register
def getHistory(request, node_id, node_type):
    node = getNode(node_id, node_type)
    path = node.getPathToRoot()
    root = getRootNode()
    history = []
    current_sn = root
    for sn, slot in reversed(path):
        history.append(createSlotList(current_sn, slot, sn))
        current_sn = sn
    slot_list = createSlotList(node, None, None) if node_type == "StructureNode" else []
    return json.dumps({"history" : history, "slot_list" : slot_list})

@dajaxice_register
def getTopRatedAlternatives(request, node_id, k = 5):
    print(0)
    current_slot = Slot.objects.get(pk=node_id)
    # get alternatives sorted by rating
    print(current_slot)
    alternatives = current_slot.node_set.order_by("-rating")
    print(alternatives)
    # TODO: prune uninteresting old nodes
    # get top k nodes
    anchor_nodes = alternatives[:min(k, len(alternatives))]
    # TODO: resort them to avoid crossings
    results = {"Anchors": [{'id': n.id, 'type' : n.as_leaf_class().getType(), 'consent': n.rating, 'total_votes': n.total_votes} for n in anchor_nodes]}
    # TODO: get all sources and derivates sorted by rating
    # TODO:
    return json.dumps(results)
