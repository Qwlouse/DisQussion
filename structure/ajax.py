#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from dajaxice.decorators import dajaxice_register
from django.template.context import RequestContext
from django.template.loader import render_to_string
import operator
from structure.forms import VotingForm, CreateTextForm
from structure.models import TextNode, Slot, StructureNode, Vote
import json
from structure.path_helpers import getRootNode
from structure.query_helpers import getTopRatedAlternatives
from structure.vote_helpers import vote_for_textNode, vote_for_structure_node
from django.db.models import Max, Min, Avg

def getNodeText(node, request):
    if isinstance(node, TextNode):
        return render_to_string('node/renderTextNode.html',
            {'title' : node.getShortTitle(),
             'text'  : node.getText(),
             'dbID'  : node.id,
             'parentID' : node.parent_id,
             'consent_rating' : node.calculate_consent_rating(),
             'wording_rating' : node.calculate_wording_rating()},
            RequestContext(request))

    elif isinstance(node, StructureNode):
        createTextForm = CreateTextForm({'slot_id' : node.parent_id})
        slots = node.slot_set.all()
        slots_info = [{'short_title' : slots[0].getShortTitle(), 'text' : slots[0].getText(), 'path' : slots[0].getTextPath()}]
        slots_info += [{'short_title' : s.getShortTitle(), 'text' : s.getText(1), 'path' : s.getTextPath()} for s in slots[1:]]

        return render_to_string('node/renderStructureNode.html',
            {'title' : node.getShortTitle(),
             'consent_rating' : node.calculate_consent_rating(),
             'wording_rating' : node.calculate_wording_rating(),
             'dbID' : node.id,
             'slots' : slots_info,
             'create_text_form' : createTextForm},
            RequestContext(request))
    else :
        return ""

def getVotingInfo(node, request):
    consent = 100
    wording = 100
    consistent = False
    if request.user.is_authenticated():
        if isinstance(node, TextNode):
            votes = Vote.objects.filter(user = request.user, text=node)
            if votes :
                vote = votes[0]
                consent = vote.consent
                wording = vote.wording
                consistent = True
        elif isinstance(node, StructureNode):
            textnodes = node.get_active_subtree()
            # check if there is already a vote
            votes = Vote.objects.filter(user=request.user, text__in=textnodes)
            a = votes.aggregate(Min('consent'), Avg('consent'),
                                Min('wording'), Avg('wording'))
            if not (0 < votes.count() < len(textnodes)) :
                if a['consent__min'] == a['consent__avg'] and\
                   a['wording__min'] == a['wording__avg']:
                    consistent = True
            consent = a['consent__avg']
            wording = a['wording__avg']
        else:
            print("This is a Slot. That shouldn't be.")
    return {"consent" : consent,
            "wording" : wording,
            "id" : node.id,
            "consistent" : consistent}

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
                       'voting' : getVotingInfo(node, request),
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
    return json.dumps({"graph_data" : getDataForAlternativesGraph(request, node.parent),
                       "voting_data" : {"consent" : consent, "wording" : wording, "id" : text_id, "consistent" : True}})

@dajaxice_register
def submitVoteForStructureNode(request, node_id, consent, wording):
    user = request.user
    node = StructureNode.objects.get(id=node_id)
    vote_for_structure_node(user, node, consent, wording)
    return json.dumps({"graph_data" : getDataForAlternativesGraph(request, node.parent),
                       "voting_data" : {"consent" : consent, "wording" : wording, "id" : node_id, "consistent" : True}})

def createSlotList(structure_node, selected_slot, selected_alternative):
    slot_list = structure_node.slot_set.order_by("pk")
    return [{'title' : s.getShortTitle() if s != selected_slot else selected_alternative.getShortTitle(),
             'id' : s.pk,
             'path' :  s.getTextPath() if s != selected_slot else selected_alternative.getTextPath(),
             'selected' : s == selected_slot} for s in slot_list]

@dajaxice_register
def getNavigationData(request, node_id, node_type):
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

def getGraphInfoForNode(node):
    return {'id': node.id,
            'nr_in_parent' : node.nr_in_parent(),
            'type' : node.as_leaf_class().getType(),
            'consent': node.rating,
            'total_votes': node.total_votes}


@dajaxice_register
def getDataForAlternativesGraph(request, node_id, k = 5):
    top_nodes = getTopRatedAlternatives(node_id, k)
    results = {"Anchors": [getGraphInfoForNode(n) for n in top_nodes]}
    # add sources and derivates
    sources_and_derivates = set()
    for node in top_nodes:
        #node = node.as_leaf_class()
        if isinstance(node, TextNode):
            sources_and_derivates = sources_and_derivates.union(set(node.sources.filter(parent=node.parent)))
            sources_and_derivates = sources_and_derivates.union(set(node.derivates.filter(parent=node.parent)))
    sources_and_derivates = sources_and_derivates.difference(set(top_nodes))
    node_add_list = sorted(sources_and_derivates, key=operator.attrgetter('rating'), reverse=True)
    node_add_list = node_add_list[:min(k, len(node_add_list))]
    results['related_nodes'] = [getGraphInfoForNode(n) for n in node_add_list]
    # add connections
    nodes = set(top_nodes + node_add_list)
    connections = []
    for n in nodes :
        if isinstance(n, TextNode):
            connections += [(s.id, n.id) for s in n.sources.all() if s in nodes]
            connections += [(n.id, d.id) for d in n.derivates.all() if d in nodes]
    results['connections'] = connections
    return json.dumps(results)
