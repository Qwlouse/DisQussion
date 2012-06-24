#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.contrib.auth.models import User

from django.db import models

short_title_max_length = 20

class Node(models.Model):
    parent = models.ForeignKey("Slot", null=True, blank=True)

    def nr_in_parent(self):
        if self.parent is None:
            return 0
        # count the number of siblings that have lower or equal id
        return self.parent.node_set.filter(id__lte=self.id).count()


class Slot(models.Model):
    parent = models.ForeignKey("StructureNode")
    short_title = models.CharField(max_length=short_title_max_length) #todo: disallow null

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


class Vote(models.Model):
    user = models.ForeignKey(User)
    text = models.ForeignKey(TextNode)
    # TODO: encode value of vote
    # TODO: ensure you cannot vote up AND down
    # TODO: ensure you can only vote once (maybe user+text = primary key)