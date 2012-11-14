#!/usr/bin/python
# -*- coding: utf-8 -*-
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.template import RequestContext
from structure.models import Vote
from structure.query_helpers import getNode
from microblogging.models import Entry, EntryReference, getFeedForUser
from view_helpers import convertVoteToVoteInfo, convertEntryToBlogPost, convertReferenceToBlogPost
import json

@dajaxice_register
def getAllActivities(request, no=0):
    if request.user.is_authenticated():
        recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.filter(user=request.user).order_by("-time")]
        feed_entries, feed_references = getFeedForUser(request.user)
        recentEntries = [convertEntryToBlogPost(e) for e in feed_entries]
        recentReferences = [convertReferenceToBlogPost(r, e) for r, e in feed_references]
    else:
        recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.all().order_by("-time")]
        recentEntries = [convertEntryToBlogPost(e) for e in Entry.objects.all().order_by("-time")]
        recentReferences = []
    activities = sorted(recentVotes + recentEntries + recentReferences, key=lambda x: -x["plain_time"])
    render_activities = activities[min(len(activities),no):min(len(activities),no+25)]
    return json.dumps({"html": render_to_string("microblogging/renderMicroblogging.html", {"activities": render_activities},
                               context_instance=RequestContext(request)),
                       "until_no": no + 25})

@dajaxice_register
def getNodeActivities(request, id, type, no=0):
    node = getNode(id, type)
    activities = [convertEntryToBlogPost(e) for e in node.references.order_by("-time")]
    render_activities = activities[min(len(activities),no):min(len(activities),no+25)]
    return json.dumps({"html": render_to_string("microblogging/renderMicroblogging.html", {"activities" : render_activities},
                               context_instance=RequestContext(request)),
                       "until_no": no + 25})

@dajaxice_register
def follow(request, username):
    user_to_follow = User.objects.filter(username = username)[0]
    request.user.userprofile.following.add(user_to_follow)
    return "1"+username

@dajaxice_register
def unfollow(request, username):
    user_to_follow = User.objects.filter(username = username)[0]
    request.user.userprofile.following.remove(user_to_follow)
    return "0"+username

@dajaxice_register
def reference(request, id):
    reference = EntryReference()
    reference.entry = Entry.objects.filter(id=id)[0]
    reference.user = request.user
    reference.save()
    return str(id)