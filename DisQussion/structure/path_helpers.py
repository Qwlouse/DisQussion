#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from models import StructureNode


def splitComponent(component):
    """
    Split a component of the form 'AAA.12' into a pair ('AAA', 12).
    If no number exists, i.e. the path is 'AAAA' return ('AAAA', -1).
    May throw an ValueError if the path is not well formed.
    """
    s = component.split('.', 1)
    if len(s) == 1:
        return s[0], -1
    else:
        return s[0], int(s[1])

def splitPath(path):
    """
    Split a path of the form 'AAA.123/BBBB.12/CC.1234/' into pairs of (short_title, nr_in_parent).
    """
    components = path.strip('/').split('/')
    return [splitComponent(c) for c in components]

def getSlot(structure_node, slot_name):
    """
    Returns the slot with the given name of the given structure_node.
    Raises ObjectDoesNotExist exception if slot is not found.
    Raises MultipleObjectsReturned exception if more than one slot is found.
    """
    matching_slot_nodes = structure_node.slot_set.filter(short_title=slot_name)
    if len(matching_slot_nodes) < 1:
        raise ObjectDoesNotExist("Error: Slot with name '%s' does not exist in StructureNode '%s'"%(slot_name, structure_node))
    if len(matching_slot_nodes) > 1:
        raise MultipleObjectsReturned("Error: StructureNode '%s' contains two or more Slots with name '%s'"%(structure_node, slot_name))
    return matching_slot_nodes[0]

def getChildWithNr(slot, nr):
    """
    Return the child node (either TextNode or StructureNode) with nr_in_parent == nr.

    """
    child_nodes = slot.node_set.order_by('id')
    if len(child_nodes) < nr:
        raise ObjectDoesNotExist("Error: Slot with name '%s' does not have a child with nr '%d'"%(slot, nr))
    return child_nodes[nr-1]

def getNodeForPath(path):
    """
    Use a path of the form 'AAA.123/BBBB.12/CC.1234/' to get the corresponding text- or structureNode from the DB.
    """
    address = splitPath(path)
    root = StructureNode.objects.filter(parent=None)[0]
    current_node = root
    for short_title, nr_in_parent in address:
        slot = getSlot(current_node, short_title)
        current_node = getChildWithNr(slot, nr_in_parent)

    return current_node