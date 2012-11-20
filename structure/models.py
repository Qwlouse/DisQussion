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
voting_bias = 10

############################## Validators #####################################
def validate_vote_value(value):
    if value not in [-1, 0, 1]:
        raise ValidationError(u'%s is not in the interval [-1:1].' % value)


############################## Tree Structure #################################
class Node(models.Model):
    parent = models.ForeignKey("Slot", null=True, blank=True)
    consent_cache = models.FloatField(default=0.0)
    wording_cache = models.FloatField(default=0.0)
    total_votes   = models.IntegerField(default=voting_bias)
    rating = models.FloatField(default=0.5)

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

    def getPathToRoot(self):
        """
        Return path to root node. Path is returned as list of tuples (StructureNode, Slot).
        """
        currentNode = self
        path = []
        while currentNode.parent is not None:
            path.append((currentNode, currentNode.parent))
            currentNode = currentNode.parent.parent
        return path

    def getTextPath(self):
        """
        Build a path string of the form 'AAA.123/BBBB.12/CC.1234'.
        """
        return "/" + "/".join("{}.{}".format(slot.short_title, sn.nr_in_parent()) for sn, slot in reversed(self.getPathToRoot()))

    def getText(self, level=0):
        """
        Traverse the subtree spanned by this node and gather the texts with highest consent.
        """
        return self.as_leaf_class().getText(level)

    def get_active_subtree(self, include_structure_nodes=False):
        return self.as_leaf_class().get_active_subtree(include_structure_nodes)

    def getShortTitle(self):
        if self.parent is None:
            return "Root"
        else :
            return self.parent.getShortTitle()  + "." + str(self.nr_in_parent())

    def calculate_consent_rating(self):
        return self.consent_cache / (2 * self.total_votes) + 0.5

    def calculate_wording_rating(self):
        return self.wording_cache / (2 * self.total_votes) + 0.5


class Slot(models.Model):
    parent = models.ForeignKey("StructureNode")
    short_title = models.CharField(max_length=short_title_max_length)
    consent_cache = models.FloatField(default=0.0)
    wording_cache = models.FloatField(default=0.0)
    total_votes   = models.IntegerField(default=0)
    rating = models.FloatField(default=0.5)

    def child_cnt(self):
        return self.node_set.count()

    def __unicode__(self):
        return self.short_title

    def getPathToRoot(self):
        return [(self,self)]+self.parent.getPathToRoot() #TODO: is (self,self) correct? Not sure if this could cause errors.

    def getTextPath(self):
        parent_path = self.parent.getTextPath()
        if not parent_path.endswith("/") :
            parent_path += "/"
        return parent_path + self.short_title

    def getText(self, level=0):
        alternatives = self.node_set.order_by('-rating')
        if not alternatives :
            return ""
        else :
            return alternatives[0].as_leaf_class().getText(level)

    def get_active_subtree(self, include_structure_nodes=False):
        alternatives = self.node_set.order_by('-rating')
        if not alternatives :
            return []
        else :
            return alternatives[0].as_leaf_class().get_active_subtree(include_structure_nodes)


    def getShortTitle(self):
        return self.short_title

    def getType(self):
        return "Slot"

    def as_leaf_class(self):
        return self


class TextNode(Node):
    text = models.TextField()
    sources = models.ManyToManyField('self', symmetrical=False, related_name="derivates", blank=True)

    def __unicode__(self):
        if self.parent is not None:
            return self.parent.short_title + "." + str(self.nr_in_parent())
        else:
            return "Unpositioned TextNode"

    def getText(self, level=0):
        return "="*level + self.text

    def getType(self):
        return "TextNode"

    def get_active_subtree(self, include_structure_nodes=False):
        return [self]


class StructureNode(Node):
    def __unicode__(self):
        if self.parent is None:
            return "ROOT"
        else:
            return self.parent.short_title + "." + str(self.nr_in_parent())

    def slot_cnt(self):
        return self.slot_set.count()

    def getText(self, level=0):
        return "\n".join(self.getPassages(level))

    def get_active_subtree(self, include_structure_nodes=False):
        subtree = [self] if include_structure_nodes else []
        for s in self.slot_set.all():
            subtree += s.as_leaf_class().get_active_subtree(include_structure_nodes)
        return subtree

    def getPassages(self, level=0):
        slots = self.slot_set.all()
        passages = [slots[0].getText(level)] + [slot.getText(level+1) for slot in slots[1:]]
        return passages

    def getType(self):
        return "StructureNode"


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




def calculate_vote_cache_TextNode(node):
    """
    Recount the votes associated with the TextNode node and write result to consent_cache and wording_cache.
    """
    node.consent_cache = Vote.objects.filter(text=node).aggregate(Sum('consent'))['consent__sum'] or 0
    node.wording_cache = Vote.objects.filter(text=node).aggregate(Sum('wording'))['wording__sum'] or 0
    node.total_votes = Vote.objects.filter(text=node).count() + voting_bias
    node.rating = node.calculate_consent_rating()
    node.save()

def calculate_vote_cache_Slot(slot):
    """
    Recalculate the consent_ and wording_cache as the maximum of the current values for the child nodes.
    """
    alternatives = slot.node_set.order_by('-rating')
    if alternatives :
        best_node = alternatives[0]
        slot.consent_cache = best_node.consent_cache
        slot.wording_cache = best_node.wording_cache
        slot.total_votes = best_node.total_votes
        slot.rating = best_node.rating
    else:
        slot.consent_cache = 0
        slot.wording_cache = 0
        slot.total_votes = 0
        slot.rating = 0.5
    slot.save()

def calculate_vote_cache_StructureNode(structureNode):
    """
    Recalculate the consent_ and wording_cache as the average over the current values for the slots.
    """
    structureNode.consent_cache = structureNode.slot_set.aggregate(Sum('consent_cache'))["consent_cache__sum"]
    structureNode.wording_cache = structureNode.slot_set.aggregate(Sum('wording_cache'))["wording_cache__sum"]
    structureNode.total_votes = structureNode.slot_set.aggregate(Sum('total_votes'))["total_votes__sum"]
    structureNode.rating = structureNode.calculate_consent_rating()
    structureNode.save()

def adjust_vote_caches(node):
    """
    Traverse the path from the given TextNode up to the root and recalculate the vote caches.
    """
    path = node.getPathToRoot()
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
