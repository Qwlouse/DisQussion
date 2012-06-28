#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.forms.models import ModelForm
from django.contrib.auth.models import User
from accounts.models import UserProfile

class EMailForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class DescriptionForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description',)