from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# copied from here: http://gitorious.org/microblog-demo/mainline/trees/master

class Entry(models.Model):
    content = models.CharField(max_length=140)
    time = models.DateTimeField('date posted')
    user = models.ForeignKey(User, related_name='entries')

    def __unicode__(self):
        return u'%s says "%s" on %s' % (self.user.username, self.content, self.time)

    class Meta(object):
        verbose_name_plural = "entries"
        ordering = ['-time']
        get_latest_by = 'time'


def getFeedForUser(user):
    return Entry.objects.filter(user__followers=user).order_by('-time')