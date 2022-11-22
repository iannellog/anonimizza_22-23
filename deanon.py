# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 17:38:22 2022

Con questo programma si rende possibile eseguire il processo di deanonimizzazione
di un file che era stato precedentemente anonimizzato con il main.

@author: danie
"""


from json import load, dump
from argparse import ArgumentParser

def deassociazione_codice(codice, tabella):
    """
#     :param codice: str
#                     il codice dell'utente del log
#     :param tabella: dict di codici
#                     la tabella di associazione ('nome':codice)
#     :return: Nome utente
#     """
    name = ' '
    for key, values in tabella.items():
       if values == codice:
          name = key
    return name



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
    
parser = ArgumentParser(description="Programma che de-anonimizza una lista di log avendo a disposizione una tabella che colleghi codice ed utente")
parser.add_argument('file_input',
                    help='Path del file da de-anonimizzare',
                    type=str)
parser.add_argument('-t','--tab_input',
                    help='Path del file da cui prendere la tabella (nome-codice)',
                    type=str,
                    default=None)
parser.add_argument('-o', '--file_output',
                    help='Path del file in cui salvare la lista de-anonimizzata; se non indicato, il default è ./results/test1_de-anonimizzato.json',
                    type=str,
                    default='./results/test1_de-anonimizzato.json')



args = parser.parse_args()


# lettura dei file di input
lista_log = leggi_file(args.file_input) # lettura file di log (lista di liste di stringhe)
tab = leggi_file(args.tab_input)

# lista_log = leggi_file('./results/anonimizzato_test1.json') # lettura file di log (lista di liste di stringhe)
# tab = leggi_file('./results/tabella_nome_codice.json')

# per ogni log procedere alla deanonimizzazione
for log in lista_log:
    log[1] = deassociazione_codice(log[1], tab)
    # for key, values in tab.items():
    #     if values == log[1]:
    #         log[1] = key
    # controlla se il codice è nella tabella
    # sostituisce in lista_log il codice del log con il nome originale
    # log[1] = deassociazione_codice(log[1], tab)  # modifica il valore anche nella lista_log


# salvare il file di log anonimizzato e la tabella
scrivi_file(args.file_output, lista_log)

