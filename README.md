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
Per la versione client (GUI) è sufficiente eseguire il comando e si aprirà una finestra di sistema per la selezione del file da processare;

Per la versione server (CLI) oltre al nome dello script sarà necessario riportare, a fianco dello script, il path del file da processare, per esempio:
```
python nome_file.py test.xlsx
```
Si consiglia di tenere tutti i file da processare all'interno di una cartella, per esempio `/input`, per avviare lo script si potrà quindi procedere con il comando `python nome_file.py input/test.xlsx`

All'interno della stessa cartella comparirà un file omonimo al file processato con l'aggiunta `_document_metadata`
