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
    with open("initial_data_storage/wahlprogramm.txt", 'r') as f:
        wahlprogramm_text = f.read()
    parseWiki(bildung, unicode(wahlprogramm_text, encoding='utf-8'))

    # Bildungsstreik Positionspapier
    with open("initial_data_storage/bildungsstreik-positionspapier.txt", 'r') as f:
        bilstr_posp_text = f.read()
    parseWiki(bildung, unicode(bilstr_posp_text, encoding='utf-8'))

    # Oktoberkonzept
    with open("initial_data_storage/oktoberkonzept.txt", 'r') as f:
        oktoberkonzept_text = f.read()
    parseWiki(bildung, unicode(oktoberkonzept_text, encoding='utf-8'))

    # Konzept AG Bildung
    bildung_ag = StructureNode()
    bildung_ag.parent = lookupNode(bildung, Slot)
    bildung_ag.save()

    grundsaetze = createSlot(bildung_ag, "Grundsaetze")
    with open("initial_data_storage/modul01.txt", 'r') as f:
        modul01_text = f.read()
    modul01 = parseWiki(grundsaetze, unicode(modul01_text, encoding='utf-8'))
    with open("initial_data_storage/modul01b_schulpflicht.txt", 'r') as f:
        modul01b_text = f.read()
    parseWiki(modul01.slot_set.all()[2], unicode(modul01b_text, encoding='utf-8'))

    bildungssystem = createSlot(bildung_ag, "Bildungssystem")
    with open("initial_data_storage/modul02.txt", 'r') as f:
        modul02_text = f.read()
    modul02 = parseWiki(bildungssystem, unicode(modul02_text, encoding='utf-8'))
    with open("initial_data_storage/modul02a3_verpflichtendes_letztes_kindergartenjahr.txt", 'r') as f:
        modul02a3_kitajahr_text = f.read()
    parseWiki(modul02.slot_set.all()[1].as_leaf_class().node_set.all()[0].as_leaf_class().slot_set.all()[3], unicode(modul02a3_kitajahr_text, encoding='utf-8'))
    with open("initial_data_storage/modul02c_ganztagsunterricht.txt", 'r') as f:
        modul02c_ganztag_text = f.read()
    parseWiki(modul02.slot_set.all()[3], unicode(modul02c_ganztag_text, encoding='utf-8'))
    with open("initial_data_storage/modul02c_gesamtschule.txt", 'r') as f:
        modul02c_gesamtschul_text = f.read()
    parseWiki(modul02.slot_set.all()[3], unicode(modul02c_gesamtschul_text, encoding='utf-8'))
    with open("initial_data_storage/modul02e_akkreditierung.txt", 'r') as f:
        modul02e_akk_text = f.read()
    parseWiki(modul02.slot_set.all()[5], unicode(modul02e_akk_text, encoding='utf-8'))

    bildungsinhalte = createSlot(bildung_ag, "Bildungsinhalte")
    with open("initial_data_storage/modul03a-c.txt", 'r') as f:
        modul03ac_text = f.read()
    modul03ac = parseWiki(bildungsinhalte, unicode(modul03ac_text, encoding='utf-8'))
    with open("initial_data_storage/modul03d.txt", 'r') as f:
        modul03d_text = f.read()
    createSlot(modul03ac, "Einh_Vor_u_Bew", unicode(modul03d_text, encoding='utf-8')) # TODO: Dies ist eine Einfügung. Durch diese Art der Speicherung wird es aber Teil des Texts.

    erwachsenenbildung = createSlot(bildung_ag, "Erwachsenenbildung")
    with open("initial_data_storage/modul04.txt", 'r') as f:
        modul04_text = f.read()
    parseWiki(erwachsenenbildung, unicode(modul04_text, encoding='utf-8'))

    schuldemokratie = createSlot(bildung_ag, "Schuldemokratie")
    with open("initial_data_storage/modul05.txt", 'r') as f:
        modul05_text = f.read()
    parseWiki(schuldemokratie, unicode(modul05_text, encoding='utf-8'))

    hochschuldemokratie = createSlot(bildung_ag, "Hochschuldemokratie")
    with open("initial_data_storage/modul06.txt", 'r') as f:
        modul06_text = f.read()
    parseWiki(hochschuldemokratie, unicode(modul06_text, encoding='utf-8'))

    lizenzfreiheit = createSlot(bildung_ag, "Lizenzfreiheit")
    with open("initial_data_storage/modul07.txt", 'r') as f:
        modul07_text = f.read()
    parseWiki(lizenzfreiheit, unicode(modul07_text, encoding='utf-8'))

    entlastungen = createSlot(bildung_ag, "Entlastungen")
    with open("initial_data_storage/modul08.txt", 'r') as f:
        modul08_text = f.read()
    parseWiki(entlastungen, unicode(modul08_text, encoding='utf-8'))
