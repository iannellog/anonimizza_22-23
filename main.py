#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:00:02 2022

@author: iannello

programma che anonimizza una lista di log e salva la corrispondenza
tra nomi e codici assegnati
""" 

from json import load, dump
  
# leggere il file di log (lista di liste di stringhe)
fin = open('./test_data/anonimizza_test1.json')
lista_log = load(fin)
fin.close()

# creare un dizionario vuoto che rappresenta la tabella (codice, nome)
tab = {}

# inizializzare il generatore di codici
codice = 0

# per ogni log procedere all'anonimizzazione
for log, i in zip(lista_log, range(len(lista_log))):
    # se il nome non è nella tabella
    if not log[1] in tab.keys():
        # generare un nuovo codice e inserire la coppia (nome, codice) nella tabella
        codice += 1
        tab[log[1]] = codice
    # sostituire il nome con il codice
    log[1] = tab[log[1]]
    # eliminare il campo "utente coinvolto"
    lista_log[i] = log[0:2] + log[3:]

# salvare il file di log anonimizzato
fout = open('./test1_anonimizzato.json','w')
dump(lista_log, fout, indent=3)
fout.close()

# salvare la tabella (nome, codice)
fout = open('./tabella_nome_codice.json','w')
dump(tab, fout, indent=3)
fout.close()

