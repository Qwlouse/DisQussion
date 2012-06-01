#!/usr/bin/python
# coding=utf-8
from django import forms

class CreateTextForm(forms.Form):
    shortTitle = forms.CharField(max_length=20,
        label="Kurztitel (20 Zeichen)",
        help_text="Kuztitel, der als Tag verwendet und im Graphen angezeigt wird. Der Kurztitel darf maximal 20 Zeichen lang sein.")
    text = forms.SlugField(widget=forms.Textarea)