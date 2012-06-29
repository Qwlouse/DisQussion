#!/usr/bin/python
# coding=utf-8
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.template import RequestContext
from django.contrib.auth.models import User
from accounts.forms import EMailForm, DescriptionForm
from structure.models import Vote

from django.utils import timezone
from datetime import datetime


def howLongAgo(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',E-Mail: ab@c.de
    'just now', etc
    """
    now = timezone.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"


def convertVoteToVoteInfo(vote):
    voteinfo = dict()
    voteinfo["type"] = 1
    voteinfo["time"] = howLongAgo(vote.time)
    voteinfo["text_url"] = vote.text.getTextPath()
    voteinfo["title"] = vote.text.parent.short_title
    voteinfo["consent"] = vote.consent
    voteinfo["wording"] = vote.wording
    return voteinfo

def show_profile(request, user_name):
    users = User.objects.filter(username = user_name)
    if not users:
        return render_to_response("accounts/UserNotFound.html", {"not_existing_username":user_name})

    user = users[0]
    profile = user.get_profile()

    userinfo = dict()
    userinfo["name"] = user.username
    userinfo["first_name"] = user.first_name
    userinfo["last_name"] = user.last_name
    userinfo["description"] = profile.description

    # Activities
    recentVotes = [convertVoteToVoteInfo(v) for v in Vote.objects.filter(user=user).order_by("time")]
    userinfo["activities"] = recentVotes

    return render_to_response("accounts/profile.html",
            {"userinfo": userinfo,
             "authForm": AuthenticationForm(),
             "emailForm" : EMailForm(instance=user),
             "descriptionForm" : DescriptionForm(instance=profile),
             "passwordForm" : PasswordChangeForm(user),
             "this_url": ".users/" + user_name},
        context_instance=RequestContext(request))

def change_email(request):
    user = request.user
    user.email = request.POST["email"]
    user.clean()
    user.save()
    return HttpResponseRedirect(request.POST["email_change_redirect"])

def change_description(request):
    profile =  request.user.get_profile()
    profile.description = request.POST["description"]
    profile.clean()
    profile.save()
    return HttpResponseRedirect(request.POST["description_change_redirect"])