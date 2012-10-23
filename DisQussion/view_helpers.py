#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import datetime
from time import mktime


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
    vote_info = dict()
    vote_info["type"] = 1
    vote_info["plain_time"] = mktime(vote.time.timetuple())
    vote_info["time"] = howLongAgo(vote.time)
    vote_info["text_url"] = vote.text.getTextPath()
    vote_info["title"] = vote.text.parent.short_title
    vote_info["consent"] = vote.consent
    vote_info["wording"] = vote.wording
    return vote_info


def convertEntryToBlogPost(entry):
    post = dict()
    post["type"] = 0
    post["plain_time"] = mktime(entry.time.timetuple())
    post["time"] = howLongAgo(entry.time)
    post["text"] = entry.content
    post["username"] = entry.user.username
    return post


def convertReferenceToBlogPost(reference, entry):
    post = dict()
    post["type"] = 2
    post["plain_time"] = mktime(reference.time.timetuple())
    post["time"] = howLongAgo(entry.time)
    post["text"] = entry.content
    post["original_author"] = entry.user.username
    post["username"] = reference.user.username
    return post