#!/usr/bin/python
# coding=utf-8
from django import forms

class CreateTextForm(forms.Form):
    shortTitle = forms.CharField(max_length=20,
        label="Kurztitel (20 Zeichen)",
        help_text="Kuztitel, der als Tag verwendet und im Graphen angezeigt wird. Der Kurztitel darf maximal 20 Zeichen lang sein.")
    text = forms.CharField(widget=forms.Textarea)

CONSENT_CHOICES = ((-1, 'Ablehnung'), (0, 'Enthaltung'), (1,  'Zustimmung'))
WORDING_CHOICES = ((-1, 'Unlesbar'), (0, 'Enthaltung'), (1,  'Lesenswert'))

class VotingForm(forms.Form):
    consent = forms.MultipleChoiceField(label='Zustimmung', widget=forms.RadioSelect, choices=CONSENT_CHOICES, required=False)
    wording = forms.MultipleChoiceField(label='Formulierung', widget=forms.RadioSelect, choices=WORDING_CHOICES, required=False)
    text_id = forms.IntegerField(widget=forms.HiddenInput())

class CreateTextNodeForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=False)
    slot_id = forms.IntegerField(widget=forms.HiddenInput)
