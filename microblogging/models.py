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


def getFeedForUser(user):
    followed = Q(user__followers=user)
    own = Q(user = user)
    return Entry.objects.filter(followed | own).order_by('-time')