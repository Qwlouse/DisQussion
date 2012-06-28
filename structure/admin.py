#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from structure.models import StructureNode, TextNode, Slot, Vote
from django.contrib import admin

from django.forms.models import ModelForm

class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will get validated and saved."""
        return True

class StructureNodeInline(admin.TabularInline):
    model = StructureNode
    readonly_fields =  ["parent", "slot_cnt", "consent_cache", "wording_cache"]
    extra = 0
    form = AlwaysChangedModelForm


class SlotInline(admin.TabularInline):
    model = Slot
    readonly_fields = ["child_cnt", "consent_cache", "wording_cache"]
    extra = 0

class TextNodeInline(admin.TabularInline):
    model = TextNode
    readonly_fields = ["consent_cache", "wording_cache"]
    extra = 0


class StructureNodeAdmin(admin.ModelAdmin):
    inlines = [SlotInline]
    list_display = ["__unicode__", "parent", "slot_cnt", "consent_cache", "wording_cache"]
    fields = ( ("parent", "nr_in_parent"), )
    readonly_fields = ["nr_in_parent"]
    search_fields = ["parent__short_title"]

class SlotAdmin(admin.ModelAdmin):
    fields = ["short_title", "parent", "child_cnt"]
    readonly_fields = [ "child_cnt"]
    list_display = ["short_title", "parent", "child_cnt", "consent_cache", "wording_cache"]
    inlines = [StructureNodeInline, TextNodeInline]


class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "text", "consent", "wording"]

admin.site.register(StructureNode, StructureNodeAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(TextNode)
admin.site.register(Vote, VoteAdmin)

