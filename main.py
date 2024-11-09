#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:00:02 2022

@author: iannello

Programma che anonimizza una lista di log e salva la corrispondenza tra nomi e codici assegnati


"""
# commento di prova fia2425

from json import load, dump
from argparse import ArgumentParser

import uuid


DIGITS = 16

def associazione_codice(nome, tabella):
    """
    Controlla se il nome (dell'utente del log) ha già una codifica nella tabella;
    se assente, ne genera una nuova e univoca.
    La codifica è gestita tramite un numero intero progressivo (codice) rappresentato con 4 cifre decimali:
    il primo codice è 0001, l'ultimo codice possibile è 9999.

    :param nome: str
                    il nome dell'utente del log
    :param tabella: dict di codici
                    la tabella di massociazione ('nome':codice)
    :return: None
    """
    # se il nome non è nella tabella
    if nome not in tabella.keys():
        # generare un nuovo codice e inserire la coppia (nome, codice) nella tabella
        codice = int(uuid.uuid4().hex[:DIGITS], base=16)
        tabella[nome] = codice
    return

def leggi_file(nome):
    """
    Legge il file JSON in "nome" e ne restituisce l'oggetto corrispondente

    :param nome: str
                file da leggere
    :return: l'oggetto python corrispondente al contenuto del file json
    """
    fin = open(nome)
    ogg_restituito = load(fin)
    fin.close()
    return ogg_restituito

def scrivi_file(nome, ogg_da_scrivere, indent=3):
    """
    Scrive l'oggetto passato nel file JSON indicato da "nome", con indentazione eventualmente modificabile

    :param nome: str
                file su cui scrivere
    :param ogg_da_scrivere: oggetto compatibile JSON da scrivere nel file
    :param indent: int
                parametro opzionale che indica l'indentazione con cui scrivere il file JSON
    :return: None
    """
    fout = open(nome, 'w')
    dump(ogg_da_scrivere, fout, indent=indent)
    fout.close()


# import da riga di comando
parser = ArgumentParser(description="Programma che anonimizza una lista di log e salva la corrispondenza tra nomi e codici assegnati")
parser.add_argument('file_input',
                    help='Path del file da anonimizzare',
                    type=str)
parser.add_argument('-t', '--tab_output',
                    help='Path del file in cui salvare la tabella; se non indicato, il default è ./results/tabella_nome_codice.json',
                    type=str,
                    default='./results/tabella_nome_codice.json')
parser.add_argument('-o', '--file_output',
                    help='Path del file in cui salvare la lista anonimizzata; se non indicato, il default è ./results/test1_anonimizzato.json',
                    type=str,
                    default='./results/test1_anonimizzato.json')
parser.add_argument('-i','--tab_input',
                    help='Path del file da cui prendere la tabella (nome-codice)',
                    type=str,
                    default=None)

args = parser.parse_args()

# lettura dei file di input
lista_log = leggi_file(args.file_input) # lettura file di log (lista di liste di stringhe)
if args.tab_input == None: # se presente, lettura della tabella; altrimenti crearne una vuota
    tab = {}
else:
    tab = leggi_file(args.tab_input)

# per ogni log procedere all'anonimizzazione
for log, i in zip(lista_log, range(len(lista_log))):
    # controlla se il nome è nella tabella; se no lo aggiunge e assegna un codice univoco
    associazione_codice(log[1], tab)
    # sostituisce in lista_log il nome del log con il codice indicato in tabella
    log[1] = tab[log[1]]  # modifica il valore anche nella lista_log
    # eliminare il campo "utente coinvolto"
    lista_log[i] = log[0:2] + log[3:]

# salvare il file di log anonimizzato e la tabella
scrivi_file(args.file_output, lista_log)
scrivi_file(args.tab_output, tab)
