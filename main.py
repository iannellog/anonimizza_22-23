#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:00:02 2022

@author: iannello

programma che anonimizza una lista di log e salva la corrispondenza
tra nomi e codici assegnati
""" 

from json import load, dump


def leggi_file_JSON(fname):
    # leggere il file di log fname (lista di liste di stringhe)
    fin = open(fname)
    data_to_be_read = load(fin)
    fin.close()
    return data_to_be_read


def scrivi_file_JSON(fname, data_to_be_written, indent=3):
    # salvare il file di log anonimizzato
    fout = open(fname, 'w')
    dump(data_to_be_written, fout, indent=indent)
    fout.close()


lista_log = leggi_file_JSON('./test_data/anonimizza_test1.json')

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

# salvare i dati
scrivi_file_JSON('results/test1_anonimizzato.json', lista_log)
scrivi_file_JSON('results/tabella_nome_codice.json', tab)

