# Anonimizzazione di un file di log

Scrivere un programma Python che legge una lista di log dal file “anonimizza_test1.json” . 

Ciascun elemento della lista di log è costituito dalle seguenti 9 informazioni:

- Data/Ora,
- Nome completo dell'utente
- Utente coinvolto
- Contesto dell'evento
- Componente
- Evento
- Descrizione
- Origine
- Indirizzo IP

Il programma deve anonimizzare la lista. In particolare:
- per ogni utente (campo “Nome completo dell'utente”) generare un identificatore unico (per esempio un numero progressivo) 
- sostituire nel log l’identificatore unico al nome dell’utente
- generare una tabella che mantiene l’informazione di quale identificatore è stato associato a ciascun utente (tabella che associa il nome dell'utente al codice unico a lui associato)
- eliminare da tutti i log il campo “Utente coinvolto”, che normalmente contiene la stringa “-“, ma potrebbe contenere anch’esso il nome dell’utente

Il programma infine deve salvare la lista di log anonimizzata nello stesso formato di partenza (json) e la tabella che associa ciascun utente al suo identificatore unico (anche la tabella va salvata in forato json). Il file di log anonimizzato va salvato come lista di log, e ciascun log come una lista di informazioni. 

# Modifiche da fare

Introduzione di sottoprogrammi.
I sottoprogrammi dovrebbero essere definiti in modo tale che sia facile successivamente integrare nella soluzione i seguenti miglioramenti:

- Generare identificatori anomimi degli utenti in un formato migliore (per es. un codice di lunghezza fissa)
- Ridurre dipendenze dai path dei file (per es. usare parametri da linea di comando)
- Poter anonimizzare un secondo file di log, e per gli stessi utenti voler usare gli stessi ID. Come si può generalizzare la soluzione?
- Poter effettuare la de-anonimizzazione (cioè partendo da un file anonimizzato ripristinare i nomi reali degli utenti)

# Modifiche effettuate

- Gli identificatori anomimi degli utenti sono generati usando il modulo uuid di Python e consistono in una stringa di 16 cifre; 
- I path dei file vengono passati sulla riga di comando
- E' possibile anonimizzare un secondo file di log, usando i codici già assegnati per gli stessi utenti. 
- E' stato aggiunto un secondo file di test per testare quest'ultima possibilità

# Utilizzo del pfrogramma

Il programma può essere lanciato da riga di comando con le segiuenti opzioni:

    usage: main.py [-h] [-t TAB_OUTPUT] [-o FILE_OUTPUT] [-i TAB_INPUT] file_input
    
    Programma che anonimizza una lista di log e salva la corrispondenza tra nomi e codici assegnati
    
    positional arguments:
      file_input            Path del file da anonimizzare
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TAB_OUTPUT, --tab_output TAB_OUTPUT
                            Path del file in cui salvare la tabella; se non indicato, il default è
                            ./results/tabella_nome_codice.json
      -o FILE_OUTPUT, --file_output FILE_OUTPUT
                            Path del file in cui salvare la lista anonimizzata; se non indicato, il
                            default è ./results/test1_anonimizzato.json
      -i TAB_INPUT, --tab_input TAB_INPUT
                            Path del file da cui prendere la tabella (nome-codice)
                        
Nella directory `results` sono forniti due file da anonimizzare. Per testare le funzioni sopra descritte usare i comandi:

    python main.py ./test_data/anonimizza_test1.json -o ./results/anonimizzato_test1.json -t ./results/tabella_nome_codice.json

    python main.py ./test_data/anonimizza_test2.json -o ./results/anonimizzato_test2.json -i ./results/tabella_nome_codice.json 