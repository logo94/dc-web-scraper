# IMPORTAZIONE LIBRERIE

import requests
from bs4 import BeautifulSoup as bs
import numpy as np
from time import sleep
import random
from random import randint
from csv import writer

# CREAZIONE DELLE VARIABILI CONTENENTI IL VALORE DELL'INDIRIZZO URL

url = ""  

host = ""   

  
user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
]

random_user_agent = random.choice(user_agents)

headers = {
    'User-Agent': random_user_agent
}

# CREAZIONE DI UN LOOP PER RACCOGLIERE TUTTE LE PAGINE DI UN SITO

pages = np.arange(0, 0, 1)  # il primo valore è la pagina di partenza, il secondo l'ultima pagina esistente nell'elenco, il terzo il numero di passaggi da eseguire (di default 1)

link = []   

# CREAZIONE O APERTURA DEL FILE CSV ALL'INTERNO DEL QUALE SCRIVERE I METADATI RACCOLTI

with open('file.csv', 'w+', encoding='utf8', newline='') as f:  # w: scrivi, w+: crea e scrivi, a: aggiungi valori a file esistente
    
    thewriter = writer(f) 
    
    header = [  # prima riga del file csv, vengono scritti i campi dei metadati; attivare le voci di interesse 
        'Identifier', 
        'Title', 
        'Date', 
        'Description',
        'Creator',
        'Publisher',
        'Rights',
        'Source'
        ]

    thewriter.writerow(header) 

    for page in pages: # per ogni pagina eseguire la richiesta HTTP e scaricare il testo HTML

        page = requests.get(url + str(page), headers=headers)

        if page.status_code != 200:   # se il codice della risposta è non è 200 allora
            print('Accesso Negato')
            exit()

        soup = bs(page.text, 'html.parser') # ottieni testo html

        articles = soup.find_all('div', class_="")  # trova tutti i box degli articoli

        for article in articles:    #per ogni articolo
            
            a = article.find('a', href=True)    # estrai link della pagina 
            link = host + a['href']

            req = requests.get(link)    # richiedi il link
            soup = bs(req.text, 'html.parser')  # ottieni il testo html di ogni articolo

            # Estrazione del contenuto di ogni elemento corrispondente ad un campo Dublin Core

            try:
                title = soup.find('').text
            except:
                print("")

            try:
                date = soup.find('', class_='').text
            except:
                print("")

            try:
                desc = soup.find('', class_="").text
            except:
                print("")

            try:
                creator = soup.find('', class_='').text
            except:
                print("")

            try:
                pub = soup.find('', class_='').text
            except:
                print("")

            try:
                rights = soup.find('', class_='').text
            except:
                print("")
            
            source = host

            metadata = [
                link, 
                title, 
                date, 
                desc,
                creator,
                pub,
                rights,
                source,
                ]

            thewriter.writerow(metadata) # i valori dei campi Dublin Core vengono aggiunti pagina per pagina, riga per riga

        sleep(randint(2,5)) # attendi tra 2 e 5 secondi prima di eseguire una richiesta
