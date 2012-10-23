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
    entry = models.ForeignKey(Entry, related_name='references')
    time = models.DateTimeField('date referenced', auto_now=True)
    user = models.ForeignKey(User, related_name='entry_references')

    def __unicode__(self):
        return u'%s references "%s" on %s' % (self.user.username, self.entry, self.time)


def getFeedForUser(user):
    references = EntryReference.objects.filter(user=user).order_by('-time')
    referenced_entries = set()
    references_and_entries = []
    for reference in references:
        if not reference.entry_id in referenced_entries:
            referenced_entries.add(reference.entry_id)
            references_and_entries.append((reference, reference.entry))
    followed = Q(user__followers=user)
    own = Q(user = user)
    entries = Entry.objects.filter(followed | own).order_by('-time')
    return [e for e in entries if not e.id in referenced_entries], references_and_entries