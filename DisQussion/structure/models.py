#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.contrib.auth.models import User

from django.db import models

short_title_max_length = 20

class Slot(models.Model):
    parent = models.ForeignKey("StructureNode")
    short_title = models.CharField(max_length=short_title_max_length) #todo: disallow null
    child_cnt = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super(Slot, self).__init__(*args, **kwargs)
        if self.child_cnt is None:
            self.child_cnt = 0

    def create_new_child_nr(self):
        self.child_cnt += 1
        self.save()
        return self.child_cnt

    def __unicode__(self):
        return self.short_title

class TextNode(models.Model):
    parent = models.ForeignKey(Slot)
    nr_in_parent = models.IntegerField()
    text = models.TextField()

    def __init__(self, *args, **kwargs):
        super(TextNode, self).__init__(*args, **kwargs)
        if self.nr_in_parent is None and self.parent is not None:
            self.nr_in_parent = self.parent.create_new_child_nr()


    def __unicode__(self):
        return self.parent.short_title + "." + str(self.nr_in_parent)


class StructureNode(models.Model):
    parent = models.ForeignKey(Slot, null=True)
    nr_in_parent = models.IntegerField(null=True)

    def __init__(self, *args, **kwargs):
        super(StructureNode, self).__init__(*args, **kwargs)
        if self.parent is not None:
            if self.nr_in_parent is None:
                self.nr_in_parent = self.parent.create_new_child_nr()
        else:
            self.nr_in_parent = 0

    def __unicode__(self):
        if self.parent is not None:
            return self.parent.short_title + "." + str(self.nr_in_parent)
        else:
            return "ROOT"


class Vote(models.Model):
    user = models.ForeignKey(User)
    text = models.ForeignKey(TextNode)
    # TODO: encode value of vote
    # TODO: ensure you cannot vote up AND down
    # TODO: ensure you can only vote once (maybe user+text = primary key)