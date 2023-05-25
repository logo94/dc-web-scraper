# dc-web-scraper
Script in python per estrarre in modo semi-automatico i metadati descrittivi, codificati in standard Dublin Core, di siti e pagine web 


## Installazione ##
Per l'utilizzo degli scripts è necessario aver scaricato `Python 3.8+` sul proprio dispositivo, per installare Python seguire le istruzioni riportate al seguente [link](https://www.python.org/downloads/).

Una volta eseguito il download è possibile verificare le versioni di `Python` e `pip` tramite i comandi:

```
python --version
```
```
pip --version
```

### Ambiente virtuale ###
Per non compromettere l'installazione di Python e le relative librerie è consigliabile creare un ambiente virtuale indipendente dal proprio sistema; per la creazione di un ambiente virtuale procedere come segue:

Creare l'ambiente virtuale
```
python -m venv pyenv
```

Attivare l'ambiente virtuale:
```
source pyenv/bin/activate
```

### Librerie ###
Una volta attivato l'ambiente virtuale è possibile procedere con l'installazione delle librerie necessarie

```
pip install -r requirements.txt
```


## Utilizzo ##
Una volta scaricato il repository e scaricate le librerie necessarie, per avviare lo script sarà sufficiente eseguire il comando:
```
python nome_file.py
```
Per la versione client (GUI) si aprirà una finestra di sistema per la selezione del file da processare;

La versione server (CLI) comunica direttamente con l'API di Archive-it, è quindi necessario disporre di un account Archive-it e del relativo token di accesso. 

Una volta installate le librerie e modificato il file `.env` inserendo il proprio token, sarà sufficiente lanciare lo script
```
python arcapi.py
```
una volta avviato verrà chiesto di inserire il Crawl_ID in modo da accedere al relativo Crawl Report e scaricare automaticamente gli URL da processare. 

Una volta completata l'operazione, all'interno della stessa cartella verrà creato un file `Crawl_ID_document_metadata.csv` contenente i metadati inclusi nei metatags dei siti archiviati.
