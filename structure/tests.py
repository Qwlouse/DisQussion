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

    def test_three_headings_results_in_TextNode(self):
        s = "Introduction\n==== Heading 1 ====\nMy name is Harry.\n=== Heading 2 ===\nI'm quite an idiot.\n== Heading 3 ==\nI reversed the ordering of the headings."
        titles = ["Einleitung", "Heading_3"]
        textparts = ["= TestSlot =\nIntroduction\n==== Heading 1 ====\nMy name is Harry.\n=== Heading 2 ===\nI'm quite an idiot.\n",
                     "=   Heading 3   =\n\nI reversed the ordering of the headings."]
        n = parse(s, self.test_slot)
        self.assertEqual(n.getType(), "StructureNode")
        for i, slot in enumerate(n.slot_set.all()):
            self.assertEqual(slot.getType(), "Slot")
            self.assertEqual(slot.short_title, titles[i])
            self.assertEqual(slot.getText(), textparts[i])
