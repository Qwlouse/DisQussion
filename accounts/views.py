#!/usr/bin/python
# coding=utf-8
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.template import RequestContext
from django.contrib.auth.models import User
from accounts.forms import EMailForm, DescriptionForm
from structure.models import Vote
from microblogging.models import Entry

from DisQussion.view_helpers import convertVoteToVoteInfo, convertEntryToBlogPost


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
    recentEntries = [convertEntryToBlogPost(e) for e in Entry.objects.filter(user=user).order_by("time")]
    userinfo["activities"] = sorted(recentVotes + recentEntries, key=lambda x: -x["plain_time"])

    return render_to_response("accounts/profile.html",
            {"userinfo": userinfo,
             "authForm": AuthenticationForm(),
             "emailForm" : EMailForm(instance=user),
             "descriptionForm" : DescriptionForm(instance=profile),
             "passwordForm" : PasswordChangeForm(user),
             "this_url": "/.users/" + user_name},
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