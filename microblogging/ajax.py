#!/usr/bin/python
# -*- coding: utf-8 -*-
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User

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