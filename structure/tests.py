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
