#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from structure.models import Slot
from structure.path_helpers import getRootNode

from structure_parser import parse

import unittest


class StructureParserTest(unittest.TestCase):
    def setUp(self):
        self.root = getRootNode()
        self.test_slot = Slot()
        self.test_slot.short_title = "TestSlot"
        self.test_slot.parent = self.root
        self.test_slot.save()

    def test_single_heading_results_in_TextNode(self):
        s = """
        = Heading1 =
        Some Text.
        """
        n = parse(s, self.test_slot)
        self.assertEqual(n.getType(), "TextNode")

    def test_tree_headings_results_in_TextNode(self):
        s = """
        Introduction
        ==== Heading 1 ====
        My name is Harry.
        === Heading 2 ===
        I'm quite an idiot.
        == Heading 3 ==
        I reversed the ordering of the headings.
        """
        titles = ["Einleitung", "Heading_1", "Heading_2", "Heading_3"]
        textparts = ["Introduction", "My name is Harry.", "I'm quite an idiot.", "I reversed the ordering of the headings."]
        n = parse(s, self.test_slot)
        self.assertEqual(n.getType(), "StructureNode")
        for i, slot in enumerate(n.slot_set.all()):
            self.assertEqual(slot.getType(), "Slot")
            print("|"+slot.short_title+"|"+titles[i])
            self.assertEqual(slot.short_title, titles[i])
            print("|"+slot.getText()+"|")
            #self.assertEqual(slot.getText(), textparts[i])
