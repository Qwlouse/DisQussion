#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.db import transaction
from structure.factory import *

def createRoot():
    root = StructureNode()
    root.save()

@transaction.commit_on_success
def createInitialData():
    populateNodeDict()

    wahlprogramm_rlp = createSlot('root', "Wahlprogramm-RLP")

    # Wahlprogramm
    with open("initial_data_storage/wahlprogramm_rlp.txt", 'r') as f:
        wahlprogramm_text = f.read()
    parseWiki(wahlprogramm_rlp, unicode(wahlprogramm_text, encoding='utf-8'))

    # Bereich Bildung
    bildung = wahlprogramm_rlp.node_set.all()[0].as_leaf_class().slot_set.all()[6]

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

    # Grundsatzprogramm RLP
    grundsatzprogramm_rlp = createSlot('root', "Grundsatzprog-RLP")

    with open("initial_data_storage/grundsatzprogramm_rlp.txt", 'r') as f:
        gsprlp_text = f.read()
    parseWiki(grundsatzprogramm_rlp, unicode(gsprlp_text, encoding='utf-8'))

    # Positionspapiere RLP
    positionspapiere_rlp = createSlot('root', "Positionspapiere-RLP")

    with open("initial_data_storage/positionspapiere_rlp.txt", 'r') as f:
        posprlp_text = f.read()
    parseWiki(positionspapiere_rlp, unicode(posprlp_text, encoding='utf-8'))

    # Grundsatzprogramm Bundesweit
    grundsatzprogramm = createSlot('root', "Grundsatzprogramm")

    with open("initial_data_storage/grundsatzprogramm_bund.txt", 'r') as f:
        gsp_text = f.read()
    parseWiki(grundsatzprogramm, unicode(gsp_text, encoding='utf-8'))

    # Wahlprogramm BTW
    wahlprogramm_btw = createSlot('root', "Wahlprogramm_BTW")

    with open("initial_data_storage/wahlprogramm_btw.txt", 'r') as f:
        wpbtw_text = f.read()
    parseWiki(wahlprogramm_btw, unicode(wpbtw_text, encoding='utf-8'))

    # Wahlprogramm BTW
    posp_bund = createSlot('root', "Positionspapiere")

    with open("initial_data_storage/positionspapiere_bund.txt", 'r') as f:
        pospbund_text = f.read()
    parseWiki(posp_bund, unicode(pospbund_text, encoding='utf-8'))