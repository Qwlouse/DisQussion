#!/usr/bin/python
# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

from DisQussion.structure.path_helpers import getNodeForPath


def home(request):
    #return HttpResponse("Hello, world. You're at the poll index.")
    return render_to_response("node/show.html",
            {"pagename":"Root",
             "form": AuthenticationForm(),
             "short_title": "Root",
             "id":1, "slots":[
                {"name":"GP", "list":[{"id":2, "text":"Gibts noch nicht"}, {"id":3, "text":"Gibbet wohl"}]},
                {"name":"WP", "list":[{"id":7, "text":"WP is doof"}, {"id":8, "text":"WP is toll"}]},
                {"name":"Orga", "list":[{"id":12, "text":"LPT"}, {"id":17, "text":"Vorst. Sitz."}]}]},
        context_instance=RequestContext(request))
    
def path(request, path):
    return HttpResponse(str(getNodeForPath(path).id))

