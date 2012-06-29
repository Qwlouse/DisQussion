#!/usr/bin/python
# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

from structure.forms import CreateTextForm
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
    return render_to_response("node/show.html",
            {"pagename":"Root",
             "this_url": "/",
             "authForm": AuthenticationForm(),
             "textForm": textForm,
             "center_node_id" : root.id
             },
        context_instance=RequestContext(request))


    
def path(request, path):
    return HttpResponse(str(getNodeForPath(path).id))

