#!/usr/bin/python
# coding=utf-8
from django import forms

CONSENT_CHOICES = ((-1, 'Ablehnung'), (0, 'Enthaltung'), (1,  'Zustimmung'))
WORDING_CHOICES = ((-1, 'Unlesbar'), (0, 'Enthaltung'), (1,  'Lesenswert'))

class VotingForm(forms.Form):
    consent = forms.MultipleChoiceField(label='Zustimmung', widget=forms.RadioSelect, choices=CONSENT_CHOICES, required=False)
    wording = forms.MultipleChoiceField(label='Formulierung', widget=forms.RadioSelect, choices=WORDING_CHOICES, required=False)
    text_id = forms.IntegerField(widget=forms.HiddenInput())

class CreateTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=False)
    slot_id = forms.IntegerField(widget=forms.HiddenInput)