#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from structure.models import Slot

def getTopRatedAlternatives(slot, k = 5, order_by="-rating"):
    if isinstance(slot, int):
        current_slot = Slot.objects.get(pk=slot)
    elif isinstance(slot, Slot):
        current_slot = slot
    # get alternatives sorted by rating
    alternatives = current_slot.node_set.order_by(order_by)
    # TODO: prune uninteresting old nodes
    # get top k nodes
    top_nodes = alternatives[:min(k, len(alternatives))]
    # TODO: resort them to avoid crossings
    return top_nodes