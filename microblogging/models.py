from django.db import models

# Create your models here.
from accounts.models import UserProfile

# copied from here: http://gitorious.org/microblog-demo/mainline/trees/master

class Entry(models.Model):
    content = models.CharField(max_length=140)
    post_date = models.DateTimeField('date posted')
    owner = models.ForeignKey(UserProfile, related_name='entries')

    def __unicode__(self):
        return u'%s says "%s" on %s' % (self.owner.user.username, self.content, self.post_date)

    class Meta(object):
        verbose_name_plural = "entries"
        ordering = ['-post_date']
        get_latest_by = 'post_date'
