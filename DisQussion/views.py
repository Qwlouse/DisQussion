#!/usr/bin/python
# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

from structure.forms import CreateTextForm
from structure.path_helpers import getNodeForPath


def home(request):
    if request.method == 'POST': # If the form has been submitted...
        textForm = CreateTextForm(request.POST) # A form bound to the POST data
        if textForm.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        textForm = CreateTextForm() # An unbound form
    return render_to_response("node/show.html",
            {"pagename":"Root",
             "authForm": AuthenticationForm(),
             "this_url": "/",
             "textForm": textForm,
             "short_title": "Root",
             "id":1, "slots":[
                {"name":"GP", "list":[{"id":1, "text":"Gibts noch nicht", "parent":0},
                                      {"id":2, "text":"Gibbet wohl", "parent":0},
                                      {"id":3, "text":"Gibts nicht und das ist gut so.", "parent":1},
                                      {"id":4, "text":"Ich bin ein Troll und möchte auch zu Wort kommen.", "parent":3},
                                      {"id":5, "text":"Gibts leider noch nicht.", "parent":1}]},
                {"name":"WP", "list":[{"id":1, "text":"WP is doof", "parent":0}, {"id":2, "text":"WP is toll", "parent":0}]},
                {"name":"Orga", "list":[{"id":1, "text":"LPT", "parent":0}, {"id":2, "text":"Vorst. Sitz.", "parent":0}]}]},
        context_instance=RequestContext(request))


    
def path(request, path):
    return HttpResponse(str(getNodeForPath(path).id))

