#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from structure.models import Vote, adjust_vote_caches
from django.db.models import Sum

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

def vote_for_structure_node(user, node, consent=None, wording=None):
    # get subtree
    textnodes = node.get_active_subtree()
    all_nodes = textnodes[:]
    # check if there is already a vote
    votes = Vote.objects.filter(user=user, text__in=textnodes)
    if votes :
        #todo warn
        for v in votes:
            # overwrite values
            if consent is not None:
                v.consent = consent
            if wording is not None:
                v.wording = wording
            v.full_clean()
            v.save()
            # remove text from textnodes
            textnodes.remove(v.text)

    for n in textnodes:
        v = Vote()
        v.user = user
        v.text = n
        v.consent = 0 if consent is None else consent
        v.wording = 0 if wording is None else wording
        v.full_clean()
        v.save()

    for n in all_nodes:
        adjust_vote_caches(n)



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


