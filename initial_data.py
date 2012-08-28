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

    bildungssystem_slot = createSlot(bildung_ag, "Bildungssystem")
    bildungssystem = StructureNode()
    bildungssystem.parent = lookupNode(bildungssystem_slot, Slot)
    bildungssystem.save()
    modul02a_slot = createSlot(bildungssystem, "vorschul_Bildung")
    modul02a_structure = StructureNode()
    modul02a_structure.parent = lookupNode(modul02a_slot, Slot)
    modul02a_structure.save()
    textfile = open("initial_data_storage/modul02a1-2.txt", 'r')
    modul02a12_text = textfile.read()
    textfile.close()
    modul02a12_slot, _ = createSlot(modul02a_structure, "frei_zug_u_traegergl", modul02a12_text)
    textfile = open("initial_data_storage/modul02a3.txt", 'r')
    modul02a3_text = textfile.read()
    textfile.close()
    modul02a3_slot, modul02a3_textNode = createSlot(modul02a_structure, "Schwerpunkte", modul02a3_text)
    textfile = open("initial_data_storage/modul02a3_verpflichtendes_letztes_kindergartenjahr.txt", 'r')
    modul02a3_pflicht_text = textfile.read()
    textfile.close()
    modul02a3_pflicht_textNode = createText(modul02a3_slot, modul02a3_pflicht_text, [modul02a3_textNode])
    textfile = open("initial_data_storage/modul02b.txt", 'r')
    modul02b_text = textfile.read()
    textfile.close()
    modul02b_slot, modul02b_textNode = createSlot(bildungssystem, "Grundschule", modul02b_text)
    textfile = open("initial_data_storage/modul02c.txt", 'r')
    modul02c_text = textfile.read()
    textfile.close()
    modul02c_slot, modul02c_textNode = createSlot(bildungssystem, "weiterfuehr_Schule", modul02c_text)
    textfile = open("initial_data_storage/modul02c_gesamtschule.txt", 'r')
    modul02c_gesamtschule_text = textfile.read()
    textfile.close()
    modul02c_gesamtschule_textNode = createText(modul02c_slot, modul02c_gesamtschule_text, [modul02c_textNode])
    textfile = open("initial_data_storage/modul02c_ganztagsunterricht.txt", 'r')
    modul02c_ganztagsunterricht_text = textfile.read()
    textfile.close()
    modul02c_gesamtschule_textNode = createText(modul02c_slot, modul02c_ganztagsunterricht_text, [modul02c_textNode])

