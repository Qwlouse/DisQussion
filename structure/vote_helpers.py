#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.db.models.aggregates import Max, Avg

from structure.models import Vote
from django.db.models import Sum
from structure.path_helpers import getPathToRoot

def vote_for_textNode(user, node, consent=None, wording=None):
    # check if there is already a vote
    votes = Vote.objects.filter(user=user, text=node)
    if votes:
        # overwrite values
        v = votes[0]
        if consent is not None:
            v.consent = consent
        if wording is not None:
            v.wording = wording
        v.full_clean()
        v.save()
    else:
        # create a new vote
        v = Vote()
        v.user = user
        v.text = node
        v.consent = 0 if consent is None else consent
        v.wording = 0 if wording is None else wording
        v.full_clean()
        v.save()
    adjust_vote_caches(node)

def get_voting_result(node):
    result = {}
    consent = Vote.objects.filter(text=node).aggregate(Sum('consent'))['consent__sum']
    result['consent'] = 0 if consent is None else consent
    wording = Vote.objects.filter(text=node).aggregate(Sum('wording'))['wording__sum']
    result['wording'] = 0 if wording is None else wording
    result['total_votes'] = Vote.objects.filter(text=node).count()
    result['consent_votes_excluding_abstention'] = Vote.objects.filter(text=node).exclude(consent=0)
    result['wording_votes_excluding_abstention'] = Vote.objects.filter(text=node).exclude(wording=0)
    return result


