#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from structure.factory import *

def createRoot():
    root = StructureNode()
    root.save()

def createInitialData():
    populateNodeDict()

    bildung = createSlot('root', "Bildung")

    # Wahlprogramm
    bildung_wp = StructureNode()
    bildung_wp.parent = lookupNode(bildung, Slot)
    bildung_wp.save()
    textfile = open("initial_data_storage/wahlprogramm.txt", 'r')
    wahlprogramm_text = textfile.read()
    textfile.close()
    wp_bildung, wp_bildung_textNode = createSlot(bildung_wp, "Wahlprogramm", wahlprogramm_text)

    # Bildungsstreik Positionspapier
    bildung_posp = StructureNode()
    bildung_posp.parent = lookupNode(bildung, Slot)
    bildung_posp.save()
    textfile = open("initial_data_storage/bildungsstreik-positionspapier.txt", 'r')
    bilstr_posp_text = textfile.read()
    textfile.close()
    posp, bilstr_posp_textNode = createSlot(bildung_posp, "Bildungsstreik-Posp", bilstr_posp_text)

    # Oktoberkonzept
    bildung_okt = StructureNode()
    bildung_okt.parent = lookupNode(bildung, Slot)
    bildung_okt.save()
    textfile = open("initial_data_storage/oktoberkonzept.txt", 'r')
    oktoberkonzept_text = textfile.read()
    textfile.close()
    oktoberkonzept_slot = createSlot(bildung_okt, "Oktoberkonzept")
    oktoberkonzept_textNode = createText(oktoberkonzept_slot, oktoberkonzept_text, [wp_bildung_textNode, bilstr_posp_textNode])

    # Konzept AG Bildung
    bildung_ag = StructureNode()
    bildung_ag.parent = lookupNode(bildung, Slot)
    bildung_ag.save()
    grundsaetze_slot = createSlot(bildung_ag, "Grundsaetze")
    grundsaetze = StructureNode()
    grundsaetze.parent = lookupNode(grundsaetze_slot, Slot)
    grundsaetze.save()
    textfile = open("initial_data_storage/modul01a.txt", 'r')
    modul01a_text = textfile.read()
    textfile.close()
    modul01a_slot, modul01a_textNode = createSlot(grundsaetze, "Modul01a", modul01a_text)
    textfile = open("initial_data_storage/modul01b.txt", 'r')
    modul01b_text = textfile.read()
    textfile.close()
    modul01b_slot, modul01b_textNode = createSlot(grundsaetze, "Modul01b", modul01b_text)
    search_text = u'Alle Lernenden haben ein Anrecht auf 13 Schuljahre.'
    additional_text = u' Die Schulpflicht von 12 Jahren bleibt davon unberührt.'
    modul01b_schulpflicht_textNode = createText(modul01b_slot,
        modul01b_text.decode(encoding='utf-8').replace(search_text, search_text + additional_text),
        [modul01b_textNode])
    textfile = open("initial_data_storage/modul01c-i.txt", 'r')
    modul01ci_text = textfile.read()
    textfile.close()
    modul01ci_slot, modul01ci_textNode = createSlot(grundsaetze, "Modul01c-i", modul01ci_text)

