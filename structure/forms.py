#!/usr/bin/python
# coding=utf-8
from django import forms


class CreateTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=False)
    slot_id = forms.IntegerField(widget=forms.HiddenInput)