#!/usr/bin/python
# coding=utf-8
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from structure.ajax import getDataForAlternativesGraph, getNavigationData

from structure.forms import CreateTextForm
from structure.models import Slot
from structure.path_helpers import getNodeForPath, getRootNode


def home(request):
    if request.method == 'POST': # If the form has been submitted...
        textForm = CreateTextForm(request.POST) # A form bound to the POST data
        if textForm.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        textForm = CreateTextForm() # An unbound form
    root = getRootNode()
    anchor_nodes = json.dumps({"Anchors": [{'id': root.id, 'type' : root.getType(), 'consent': root.rating, 'total_votes': root.total_votes}] })

    return render_to_response("node/show.html",
            {"pagename":"Root",
             "this_url": "/",
             "authForm": AuthenticationForm(),
             "textForm": textForm,
             "navigation" : getNavigationData(request, root.id, root.getType()),
             "anchor_nodes" : anchor_nodes,
             "selected_id" : root.id
             },
        context_instance=RequestContext(request))


    
def path(request, path):
    if request.method == 'POST': # If the form has been submitted...
        textForm = CreateTextForm(request.POST) # A form bound to the POST data
        if textForm.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        node = getNodeForPath(path).as_leaf_class()
        if isinstance(node, Slot):
            node = node.node_set.order_by('-rating')[0].as_leaf_class()


        ## structure : Graph  : get top rated siblings and select node
        ###            Path   : path to parent select node
        ###            Content: slots
        ## text      : Graph  : get top rated siblings and select node
        ###            Path   : path to parent select node
        ###            Content: slots



        textForm = CreateTextForm() # An unbound form

        anchor_nodes = getDataForAlternativesGraph(request, node.parent_id)
        return render_to_response("node/show.html",
                {"pagename": node.getShortTitle(),
                 "this_url": node.getTextPath(),
                 "authForm": AuthenticationForm(),
                 "textForm": textForm,
                 "navigation" : getNavigationData(request, node.id, node.getType()),
                 "anchor_nodes" : anchor_nodes,
                 "selected_id" : node.id
            },
            context_instance=RequestContext(request))

