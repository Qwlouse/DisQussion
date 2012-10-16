#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

import re
from structure.models import TextNode, StructureNode, Slot


def getHeadingMatcher(level=0):
    if 0 < level < 7:
        s = "%d"%level
    elif level == 0:
        s = "1, 6"
    else:
        raise ValueError("level must be between 1 and 6 or 0, but was %d."%level)
    return re.compile(r"^\s*={%s}(?P<title>[^=§]+)(?:§\s*(?P<short_title>[^=§\s]+)\s*)?=*\s*$"%s, flags=re.MULTILINE)

h1_start = re.compile(r"^\s*=(?P<title>[^=§]+)=*\s*$", flags=re.MULTILINE)
general_h = re.compile(r"^\s*(={2,6}(?P<title>[^=]+)=*)\s*$", flags=re.MULTILINE)


def parse(s, parent_slot):
    #make sure we start with a heading 1
    m = h1_start.match(s) # TODO: match short titles and warn about
    if m :
        title = m.groups("title")[0]
        s = h1_start.sub("", s)
    else :
        # TODO: warn about missing title
        title = parent_slot.short_title

    # do we need a StructureNode or will a TextNode do?
    if not general_h.search(s) :
        # TextNode
        t = TextNode()
        t.text = "= %s =\n"%title.strip() + s.strip()
        t.parent = parent_slot
        t.save()
        print("Generated TextNode", t)
        return t
    # else : StructureNode

    node = StructureNode()
    node.parent = parent_slot
    node.save()
    print("Generated StructureNode", node)

    # determine used header depth:
    level = 0
    for i in range(2, 7):
        m = getHeadingMatcher(i)
        if m.search(s):
            level = i
            break
    assert 1 < level < 7
    print("going on to split at level", level)

    split_doc = m.split(s)
    # now the text before, between and after headings is split_doc[0::3]
    # the text of the headings are split_doc[1::3]
    # and the short titles (or None if omitted) are split_doc[2::3]
    # what do we do now?

    # leading text is used to construct an "Einleitung" Slot and TextNode
    introduction = Slot()
    introduction.parent = node
    introduction.short_title = "Einleitung"
    introduction.save()
    print("created intro node", introduction)
    introduction_text = TextNode()
    introduction_text.parent = introduction
    intro_text = split_doc[0]
    # assert that no headings are in intro-text
    if general_h.search(intro_text):
        # TODO: Warn!
        intro_text = general_h.sub(r"~\1", intro_text)
        #general_h.
    introduction_text.text = "= %s =\n"%title + intro_text
    introduction_text.save()
    print("created intro-text", introduction_text)


    # iterate the headings, short_titles, and corresponding texts:
    for title, short_title, text in zip(split_doc[1::3], split_doc[2::3], split_doc[3::3]):
        # check if short_title is valid/unique/exists
        # TODO: further validity checks
        # TODO: Check uniqueness
        if not short_title or len(short_title.strip()) == 0:
            short_title=title[:min(15, len(title))]
        slot = Slot()
        slot.parent = node
        slot.short_title = short_title.strip().replace(" ", "_")
        slot.save()
        print("Generated Slot", slot)
        parse("= %s =\n"%title.strip() + text.strip(), slot)
    return node
