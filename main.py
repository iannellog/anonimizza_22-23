#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:00:02 2022

@author: iannello

Programma che svolge una delle seguenti:
- anonimizza una lista di log e salva la corrispondenza tra nomi e codici assegnati
- de-anonimizza una lista di log a partire dal una tabella di codifica


TEST:
*** il test utilizza la cartella ./results; se non presente, viene creata
1. test di anonimizzazione semplice; con default della tabella e del file in output:
    par: ./test_data/anonimizza_test1.json
    res: ./results/file_anonimizzato.json ./results/tabella_nome_codice.json

2. test di anonimizzazione con tabella in ingresso, con output tabella specificato:
    par: ./test_data/anonimizza_test2.json -i ./results/tabella_nome_codice.json -o ./results/test2_anonimizzato.json -t ./results/tabella_nome_codice2.json
    res: ./results/test2_anonimizzato.json ./results/tabella_nome_codice2.json

3. test di de-anonimizzazione
    par: ./results/test2_anonimizzato.json -f -i ./results/tabella_nome_codice2.json -o ./results/test2_de_anonimizzato.json
    res: ./results/test2_de_anonimizzato.json (coincide con anonimizza_test2.json)
"""

from json import load, dump
from argparse import ArgumentParser
import os

def associazione_codice(nome: str, tabella: dict) -> None:
    """
    Controlla se il nome (dell'utente del log) ha già una codifica nella tabella;
    se assente, ne genera una nuova e univoca.
    La codifica è gestita tramite un numero intero progressivo (codice) rappresentato con 4 cifre decimali:
    il primo codice è 0001, l'ultimo codice possibile è 9999.

    :param nome: str
                    il nome dell'utente del log
    :param tabella: dict di codici
                    la tabella di associazione ('nome':codice)
    :return: None
    """
    # se il nome non è nella tabella
    if nome not in tabella.keys():
        # generare un nuovo codice e inserire la coppia (nome, codice) nella tabella
        numkeys = len(tabella) + 1
        codice = str(numkeys).zfill(4)
        tabella[nome] = codice
    return


def leggi_file(nome: str) -> str:
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


def scrivi_file(nome: str, ogg_da_scrivere, indent=3) -> None:
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


# parsing dell'import da riga di comando
parser = ArgumentParser(
    description="Programma che svolge una delle seguenti:\n"
                "- anonimizza una lista di log, eventualmente anche in base ad una tabella di codifica in input;"
                " salva la corrispondenza tra nomi e codici assegnati in una tabella di codifica in output;\n"
                "- de-anonimizza una lista anonimizzata in base ad una tabela di codifica specificata.")
parser.add_argument('file_input',
                    help='Path del file in cui è contenuta la lista di log.',
                    type=str)
parser.add_argument('-f',
                    help='Se presente, il programma svolge la de-anonimizzazione del file in input sulla base della tabella in input.\n'
                         'Se presente, la tabella input è obbligatoria',
                    action="store_true")  # di default è False
parser.add_argument('-i', '--tab_input',
                    help='Path del file in cui è contenuta la tabella di codifica. Parametro facoltativo nel caso di anonimizzazione,'
                         'parametro necessario ne caso di de-anonimizzazione.',
                    type=str,
                    default=None)
parser.add_argument('-t', '--tab_output',
                    help='Path del file in cui salvare la tabella in uscita (caso di anonimizzazione); '
                         'se non indicato, il default è ./results/tabella_nome_codice.json. Nel caso di de-anonimizzazione non ha alcun effetto.',
                    type=str,
                    default='./results/tabella_nome_codice.json')
parser.add_argument('-o', '--file_output',
                    help='Path del file in cui salvare la lista anonimizzata; se non indicato, il default è ./results/test1_anonimizzato.json',
                    type=str,
                    default='./results/file_anonimizzato.json')


args = parser.parse_args()

if args.tab_output == './results/tabella_nome_codice.json' or args.file_output == './results/file_anonimizzato.json':
    if not os.path.exists('./results'):
        os.mkdir('./results')

# lettura della lista di log in input (lista di liste di stringhe)
lista_log = leggi_file(args.file_input)


if not args.f:  # se è assente il flag -f
    ## programma di anonimizzazione
    # se presente la tabella in input, la legge; altrimenti crea una tabella vuota
    if args.tab_input is None:
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

else:  # se è presente il flag -f
    ## programma di de-anonimizzazione
    # errore se non viene passata una tabella di de-anonimizzazione
    if args.tab_input is None:
        exit('Errore: tabella in input non trovata.')
    tab = leggi_file(args.tab_input)
    # se la tabella è (nome-codice) la inverte, ottenendo (codice-nome)
    if list(tab.values())[0].isdigit():
        tab = {v: k for (v, k) in ((v, k) for (k, v) in tab.items())}
    # per ogni log del file anonimizzato procedere alla de-anonimizzazione
    for log, i in zip(lista_log, range(len(lista_log))):
        """ 
        # controlla che il codice sia nella tabella, altrimenti dà errore
        """
        # sostituisce in lista_log il codice del log con il nome indicato in tabella
        log[1] = tab[log[1]]  # modifica il valore anche nella lista_log

    # salvare il file di log de-anonimizzato
    scrivi_file(args.file_output, lista_log)
