#!/usr/bin/python
# coding=utf-8

from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
from django.contrib.auth.models import User
from structure.models import Vote

# Create your views here.
from structure.path_helpers import getPathForNode

def convertVoteToVoteInfo(vote):
    voteinfo = dict()
    voteinfo["time"] = vote.time
    voteinfo["text_url"] = getPathForNode(vote.text)
    voteinfo["title"] = vote.text.parent.short_title
    voteinfo["consent"] = vote.consent
    voteinfo["wording"] = vote.wording
    return voteinfo

def show_profile(request, user_name):
    users = User.objects.filter(username = user_name)
    if not users:
        return render_to_response("accounts/UserNotFound.html")

    user = users[0]
    profile = user.get_profile()

    userinfo = dict()
    userinfo["name"] = user.username
    userinfo["first_name"] = user.first_name
    userinfo["last_name"] = user.last_name
    userinfo["description"] = profile.description
    userinfo["email"] = user.email

    # Activities
    recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.filter(user=user).order_by("time")]
    userinfo["activities"] = recentVotes

    return render_to_response("accounts/profile.html",
            {"userinfo": userinfo,
             "authForm": AuthenticationForm(),
             "this_url": ".users/" + user_name},
        context_instance=RequestContext(request))