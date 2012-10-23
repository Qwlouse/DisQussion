#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import re
# copied from here: http://gitorious.org/microblog-demo/mainline/trees/master
from structure.models import Node
from structure.path_helpers import getNodeForPath

user_ref_pattern = re.compile(r"(?:(?<=\s)|\A)@(?P<username>\w+)\b")
tag_pattern = re.compile(r"(?:(?<=\s)|\A)#(?P<tagname>\w+)\b")
internal_link_pattern = re.compile(r"(?:(?<=\s)|\A)(?P<path>/(?:[a-zA-Z0-9-_]+\.\d+/)*[a-zA-Z0-9-_]+(?:\.\d+)?/?)\b")
url_pattern = re.compile(r"(?:(?<=\s)|\A)((?:https?://)?[\da-z\.-]+\.[a-z\.]{2,6}[-A-Za-z0-9+&@#/%?=~_|!:,.;]*)\b")


def create_entry(text, user):
    split_text = user_ref_pattern.split(text)
    mentions = []
    for i in range(1, len(split_text), 2):
        username = split_text[i]
        try:
            u = User.objects.get(username=username)
            split_text[i] = '<a href="/.users/{0}">@{0}</a>'.format(username)
            mentions.append(u)
        except User.DoesNotExist:
            split_text[i] = '@'+username
    text = "".join(split_text)

    split_text = tag_pattern.split(text)
    for i in range(1, len(split_text), 2):
        tagname = split_text[i]
        split_text[i] = '<a href="/.search?search_string=#{0}">#{0}</a>'.format(tagname)
    text = "".join(split_text)

    split_text = internal_link_pattern.split(text)
    nodes = []
    for i in range(1, len(split_text), 2):
        path = split_text[i]
        try:
            n = getNodeForPath(path)
            split_text[i] = '<a href="{0}">{1}</a>'.format(path, n.getShortTitle())
            nodes.append(n)
        except ObjectDoesNotExist:
            pass
    text = "".join(split_text)

    split_text = url_pattern.split(text)
    for i in range(1, len(split_text), 2):
        link = split_text[i]
        split_text[i] = '<a href="{0}">{0}</a>'.format(link)
    text = "".join(split_text)

    entry = Entry()
    entry.content = text
    entry.user = user
    entry.save()
    entry.mentions.add(*mentions)
    entry.node_references.add(*nodes)
    entry.save()
    return entry


class Entry(models.Model):
    content = models.TextField()
    time = models.DateTimeField('date posted', auto_now=True)
    user = models.ForeignKey(User, related_name='entries')
    mentions = models.ManyToManyField(User, related_name='mentioning_entries', symmetrical=False, blank=True)
    node_references = models.ManyToManyField(Node, related_name='references', blank=True)

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
