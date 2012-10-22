#!/usr/bin/python
# coding=utf-8
import json
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from structure.ajax import getDataForAlternativesGraph, getNavigationData, getGraphInfoForNode
from django.db.models import Q

from structure.models import Slot, Vote
from structure.path_helpers import getNodeForPath, getRootNode
from microblogging.models import Entry, getFeedForUser
from structure.models import TextNode
from view_helpers import convertVoteToVoteInfo, convertEntryToBlogPost


def home(request):
    root = getRootNode()
    anchor_nodes = json.dumps({"Anchors": [getGraphInfoForNode(root)],
                               "related_nodes" : [],
                               "connections" : []})
    if request.user.is_authenticated():
        recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.filter(user=request.user).order_by("time")]
        recentEntries = [convertEntryToBlogPost(e) for e in getFeedForUser(request.user)]
    else:
        recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.all().order_by("time")]
        recentEntries = [convertEntryToBlogPost(e) for e in Entry.objects.all().order_by("time")]
    activities = sorted(recentVotes + recentEntries, key=lambda x: -x["plain_time"])
    return render_to_response("index.html",
            {"pagename":"Root",
             "this_url": "/",
             "authForm": AuthenticationForm(),
             "navigation" : getNavigationData(request, root.id, root.getType()),
             "anchor_nodes" : anchor_nodes,
             "selected_id" : root.id,
             "activities" : activities
             },
        context_instance=RequestContext(request))

    
def path(request, path):
    node = getNodeForPath(path).as_leaf_class()
    if isinstance(node, Slot):
        node = node.node_set.order_by('-rating')[0].as_leaf_class()

    ## structure : Graph  : get top rated siblings and select node
    ###            Path   : path to parent select node
    ###            Content: slots
    ## text      : Graph  : get top rated siblings and select node
    ###            Path   : path to parent select node
    ###            Content: slots

    anchor_nodes = getDataForAlternativesGraph(request, node.parent_id)
    return render_to_response("node/show.html",
        {"pagename": node.getShortTitle(),
         "this_url": node.getTextPath(),
         "authForm": AuthenticationForm(),
         "navigation": getNavigationData(request, node.id, node.getType()),
         "anchor_nodes": anchor_nodes,
         "selected_id": node.id
        },
        context_instance=RequestContext(request))


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    """
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    """
    Returns a query, that is a combination of Q objects. That combination aims to search keywords within a model by
    testing the given search fields.
    """
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query &= or_query
    return query

def search(request):
    if request.method == 'GET' and 'search_string' in request.GET and request.GET['search_string'].strip():
        query_string = request.GET['search_string']
        entry_query = get_query(query_string, ['text', ])
        textNodes = TextNode.objects.filter(entry_query).order_by("-id")
        search_results = []
        for node in textNodes:
            search_results.append({"path": node.getTextPath(), "snippet": node.text[:min(len(node.text), 140)]})
        root = getRootNode()
        anchor_nodes = json.dumps({"Anchors": [getGraphInfoForNode(root)], "related_nodes": [], "connections": []})
        if request.user.is_authenticated():
            recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.filter(user=request.user).order_by("time")]
            recentEntries = [convertEntryToBlogPost(e) for e in getFeedForUser(request.user)]
        else:
            recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.all().order_by("time")]
            recentEntries = [convertEntryToBlogPost(e) for e in Entry.objects.all().order_by("time")]
        activities = sorted(recentVotes + recentEntries, key=lambda x: -x["plain_time"])
        return render_to_response("search_results.html",
            {"pagename": "Root",
             "this_url": "/",
             "authForm": AuthenticationForm(),
             "navigation": getNavigationData(request, root.id, root.getType()),
             "anchor_nodes": anchor_nodes,
             "selected_id": root.id,
             "search_string": query_string,
             "search_results": search_results,
             "activities": activities
            },
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/') # No search

