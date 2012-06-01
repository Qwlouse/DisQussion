#!/usr/bin/python
# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

from DisQussion.structure.forms import CreateTextForm
from DisQussion.structure.path_helpers import getNodeForPath


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
             "textForm": textForm,
             "short_title": "Root",
             "id":1, "slots":[
                {"name":"GP", "list":[{"id":2, "text":"Gibts noch nicht"}, {"id":3, "text":"Gibbet wohl"}]},
                {"name":"WP", "list":[{"id":7, "text":"WP is doof"}, {"id":8, "text":"WP is toll"}]},
                {"name":"Orga", "list":[{"id":12, "text":"LPT"}, {"id":17, "text":"Vorst. Sitz."}]}]},
        context_instance=RequestContext(request))
    
def path(request, path):
    return HttpResponse(str(getNodeForPath(path).id))

