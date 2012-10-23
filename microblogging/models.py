#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# copied from here: http://gitorious.org/microblog-demo/mainline/trees/master

class Entry(models.Model):
    content = models.CharField(max_length=140)
    time = models.DateTimeField('date posted', auto_now=True)
    user = models.ForeignKey(User, related_name='entries')

    def __unicode__(self):
        return u'%s says "%s" on %s' % (self.user.username, self.content, self.time)

    class Meta(object):
        verbose_name_plural = "entries"
        ordering = ['-time']
        get_latest_by = 'time'


class EntryReference(models.Model):
    entry = models.ForeignKey(Entry, related_name='+')
    time = models.DateTimeField('date posted', auto_now=True)
    user = models.ForeignKey(User, related_name='entry_references')

    def __unicode__(self):
        return u'%s references "%s" on %s' % (self.user.username, self.entry, self.time)


def getFeedForUser(user):
    followed = Q(user__followers=user)
    own = Q(user = user)
    references = EntryReference.objects.filter(user__followers=user).order_by('-time')
    referenced_entries = set()
    references_and_entries = []
    for reference in references:
        if reference.entry_id in referenced_entries:
            del reference
        else: referenced_entries.add(reference.entry_id)
        references_and_entries.append((reference, reference.entry))
    entries = Entry.objects.filter(followed | own).order_by('-time')
    for entry in entries:
        if entry.id in referenced_entries: del entry
    return entries, references_and_entries