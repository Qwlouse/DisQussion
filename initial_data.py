#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from structure.factory import *

def createRoot():
    root = StructureNode()
    root.save()

def createInitialData():
    populateNodeDict()
    gp, gp1 = createSlot('root', "GP", "Kein Grundsatzprogramm vorhanden!")
    wp, wp1 = createSlot('root', "WP", "Inhalte statt Köpfe!")

    #Bildung
    #textfile = open("initial_data_storage/modul01a.txt", 'r')
    #modul01a_text = textfile.read()
    #textfile.close()
    #bildungsprogramm = createStructure(wp,{"Grundsätze": modul01a_text})

