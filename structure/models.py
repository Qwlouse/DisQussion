#!/usr/bin/python
# coding=utf-8

############################## Imports ########################################
from __future__ import division, print_function, unicode_literals
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.aggregates import Sum, Avg, Max
from django.db.models.signals import post_save

############################## Globals ########################################
short_title_max_length = 20


############################## Validators #####################################
def validate_vote_value(value):
    if value not in [-1, 0, 1]:
        raise ValidationError(u'%s is not in the interval [-1:1].' % value)


############################## Tree Structure #################################
class Node(models.Model):
    parent = models.ForeignKey("Slot", null=True, blank=True)
    consent_cache = models.FloatField(default=0.0)
    wording_cache = models.FloatField(default=0.0)

    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base()

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if model == Node:
            return self
        return model.objects.get(id=self.id)



    def nr_in_parent(self):
        if self.parent is None:
            return 0
        # count the number of siblings that have lower or equal id
        return self.parent.node_set.filter(id__lte=self.id).count()


class Slot(models.Model):
    parent = models.ForeignKey("StructureNode")
    short_title = models.CharField(max_length=short_title_max_length) #todo: disallow null
    consent_cache = models.FloatField(default=0.0)
    wording_cache = models.FloatField(default=0.0)

    def child_cnt(self):
        return self.node_set.count()

    def __unicode__(self):
        return self.short_title


class TextNode(Node):
    text = models.TextField()

    def __unicode__(self):
        if self.parent is not None:
            return self.parent.short_title + "." + str(self.nr_in_parent())
        else:
            return "Unpositioned TextNode"


class StructureNode(Node):
    def __unicode__(self):
        if self.parent is None:
            return "ROOT"
        else:
            return self.parent.short_title + "." + str(self.nr_in_parent())

    def slot_cnt(self):
        return self.slot_set.count()


############################## Votes ##########################################
class Vote(models.Model):
    user = models.ForeignKey(User)
    text = models.ForeignKey(TextNode)
    consent = models.IntegerField(default=0, validators=[validate_vote_value])
    wording = models.IntegerField(default=0, validators=[validate_vote_value])
    time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('user', 'text')

    def __unicode__(self):
        return "{} for {} ({}, {})".format(self.user.username, self.text, self.consent, self.wording)

def getPathToRoot(node):
    """
    Return path to root node for given text or structure node. Path is returned as list of tuples (StructureNode, Slot).
    """
    currentNode = node
    path = []
    while currentNode.parent is not None:
        path.append((currentNode, currentNode.parent))
        currentNode = node.parent.parent
    return path


def calculate_vote_cache_TextNode(node):
    """
    Recount the votes associated with the TextNode node and write result to consent_cache and wording_cache.
    """
    node.consent_cache = Vote.objects.filter(text=node).aggregate(Sum('consent'))['consent__sum']
    node.wording_cache = Vote.objects.filter(text=node).aggregate(Sum('wording'))['wording__sum']
    node.save()

def calculate_vote_cache_Slot(slot):
    """
    Recalculate the consent_ and wording_cache as the maximum of the current values for the child nodes.
    """
    slot.consent_cache = slot.node_set.aggregate(Max('consent_cache'))['consent_cache__max']
    slot.wording_cache = slot.node_set.aggregate(Max('wording_cache'))['wording_cache__max']
    slot.save()

def calculate_vote_cache_StructureNode(structureNode):
    """
    Recalculate the consent_ and wording_cache as the average over the current values for the slots.
    """
    structureNode.consent_cache = structureNode.slot_set.aggregate(Avg('consent_cache'))["consent_cache__avg"]
    structureNode.wording_cache = structureNode.slot_set.aggregate(Avg('wording_cache'))["wording_cache__avg"]
    structureNode.save()

def adjust_vote_caches(node):
    """
    Traverse the path from the given TextNode up to the root and recalculate the vote caches.
    """
    path = getPathToRoot(node)
    # first pair is (TextNode, Slot)
    textNode, slot = path[0]
    calculate_vote_cache_TextNode(textNode)
    calculate_vote_cache_Slot(slot)
    if len(path) <= 1:
        return

    for structureNode, slot in path[1:]:
        calculate_vote_cache_StructureNode(structureNode)
        calculate_vote_cache_Slot(slot)

# Use signals to ensure the vote caches will be recalculated with every vote save
def save_vote(sender, instance, created, **kwargs):
    adjust_vote_caches(instance.text)

post_save.connect(save_vote, sender=Vote)
