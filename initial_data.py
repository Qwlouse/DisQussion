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
    wp_bildung = parseWiki(bildung, unicode(wahlprogramm_text, encoding='utf-8'))

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
    oktoberkonzept_textNode = createText(oktoberkonzept_slot, oktoberkonzept_text, [bilstr_posp_textNode])

    # Konzept AG Bildung
    bildung_ag = StructureNode()
    bildung_ag.parent = lookupNode(bildung, Slot)
    bildung_ag.save()

    grundsaetze_slot = createSlot(bildung_ag, "Grundsaetze")
    #grundsaetze = StructureNode()
    #grundsaetze.parent = lookupNode(grundsaetze_slot, Slot)
    #grundsaetze.save()
    with open("initial_data_storage/modul01.txt", 'r') as f:
        modul01_text = f.read()
    modul01 = parseWiki(grundsaetze_slot, unicode(modul01_text, encoding='utf-8'))
    with open("initial_data_storage/modul01b_schulpflicht.txt", 'r') as f:
        modul01b_text = f.read()
    modul01b_alt = parseWiki(modul01.slot_set.all()[2], unicode(modul01b_text, encoding='utf-8'))
    #search_text = u'Alle Lernenden haben ein Anrecht auf 13 Schuljahre.'
    #additional_text = u' Die Schulpflicht von 12 Jahren bleibt davon unberührt.'
    #modul01b_schulpflicht_textNode = createText(modul01b_slot,
    #    modul01b_text.decode(encoding='utf-8').replace(search_text, search_text + additional_text),
    #    [modul01b_textNode])

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
    textfile = open("initial_data_storage/modul02d.txt", 'r')
    modul02d_text = textfile.read()
    textfile.close()
    modul02d_slot, modul02d_textNode = createSlot(bildungssystem, "alternative_Schulen", modul02d_text)
    textfile = open("initial_data_storage/modul02e.txt", 'r')
    modul02e_text = textfile.read()
    textfile.close()
    modul02e_slot, modul02e_textNode = createSlot(bildungssystem, "Hochschule", modul02e_text)
    textfile = open("initial_data_storage/modul02e_akkreditierung.txt", 'r')
    modul02e_akkreditierung_text = textfile.read()
    textfile.close()
    modul02e_akkreditierung_textNode = createText(modul02e_slot, modul02e_akkreditierung_text, [modul02e_textNode])
    textfile = open("initial_data_storage/modul02f.txt", 'r')
    modul02f_text = textfile.read()
    textfile.close()
    modul02f_slot, modul02f_textNode = createSlot(bildungssystem, "faire_Bezahlung", modul02f_text)

    bildungsinhalte_slot = createSlot(bildung_ag, "Bildungsinhalte")
    bildungsinhalte = StructureNode()
    bildungsinhalte.parent = lookupNode(bildungsinhalte_slot, Slot)
    bildungsinhalte.save()
    textfile = open("initial_data_storage/modul03a-c.txt", 'r')
    modul03ac_text = textfile.read()
    textfile.close()
    modul03ac_slot, modul03ac_textNode = createSlot(bildungsinhalte, "Inhalte", modul03ac_text)
    modul03d_slot, modul03d_textNode = createSlot(bildungsinhalte, "Abschluesse", "")
    textfile = open("initial_data_storage/modul03d.txt", 'r')
    modul03d_text = textfile.read()
    textfile.close()
    modul03d_abschluesse_textNode = createText(modul03d_slot, modul03d_text)

    textfile = open("initial_data_storage/modul04.txt", 'r')
    modul04_text = textfile.read()
    textfile.close()
    erwachsenenbildung_slot, erwachsenenbildung_textNode = createSlot(bildung_ag, "Erwachsenenbildung", modul04_text)

    textfile = open("initial_data_storage/modul05.txt", 'r')
    modul05_text = textfile.read()
    textfile.close()
    schuldemokratie_slot, schuldemokratie_textNode = createSlot(bildung_ag, "Schuldemokratie", modul05_text)

    textfile = open("initial_data_storage/modul06.txt", 'r')
    modul06_text = textfile.read()
    textfile.close()
    hochschuldemokratie_slot, hochschuldemokratie_textNode = createSlot(bildung_ag, "Hochschuldemokratie", modul06_text)

    textfile = open("initial_data_storage/modul07.txt", 'r')
    modul07_text = textfile.read()
    textfile.close()
    lizenzfreiheit_slot, lizenzfreiheit_textNode = createSlot(bildung_ag, "Lizenzfreiheit", modul07_text)

    textfile = open("initial_data_storage/modul08.txt", 'r')
    modul08_text = textfile.read()
    textfile.close()
    entlastungen_slot, entlastungen_textNode = createSlot(bildung_ag, "Entlastungen", modul08_text)
