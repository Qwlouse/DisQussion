#!/usr/bin/python
# coding=utf-8

from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext

# Create your views here.

def show_profile(request):
    user = request.user
    profile = user.get_profile()
    return render_to_response("profile.html",
            {"user_to_show": {
            "name": user.username,
            "selfdescription": profile.description,
            "activities": [
                    {"time":"12m","type":1,"text":"Vorschlag erstellt: GP"},
                    {"time":"4h","type":0,"text":"Ich bin Twitter gewöhnt, aber das hier ist #ungewohnt."}]},
             "authForm": AuthenticationForm(),
             "this_url": "profiles/admin"},
        context_instance=RequestContext(request))