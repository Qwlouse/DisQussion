#!/usr/bin/python
# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    description = models.TextField()

# Use signals to ensure the profile will be created automatically when a user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)


# From http://stackoverflow.com/questions/1466827/ --
#
# Prevent interactive question about wanting a superuser created.
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')


# Create our own test user automatically.
def create_testuser(app, created_models, verbosity, **kwargs):
    if not settings.DEBUG:
        return
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print '*' * 80
        print 'Creating admin -- login: admin, password: 1234'
        print '*' * 80
        assert auth_models.User.objects.create_superuser('admin', 'ab@c.com', '1234')
    else:
        print 'Admin user already exists.'

signals.post_syncdb.connect(create_testuser,
    sender=auth_models, dispatch_uid='common.models.create_testuser')