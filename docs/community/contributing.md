# Contributing

## Server

Questa sezione spiega come aggiungere alla libreia la possibilità di scaricare un episodio da un'altro server non ancora supportato.

|Name|Supported|
|:---|:-------:|
|AnimeWorld_Server|✔️|
|Streamtape|✔️|
|YouTube|✔️|
|StreamHide|❌|
|FileMoon|❌|
|Streamtape|❌|
|Doodstream|❌|
|StreamSB|❌|
|Streamlare|❌|

Per aggiungere un nuovo server basta seguire questi passi:

1. Creare un file .py con il nome del server e metterlo nella cartella [servers](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/servers). (es `NuovoServer.py`)

1. Usa questo template per la classe del nuovo server: 
```py
from .Server import *

class NuovoServer(Server):
	def fileLink(self): # Obbligatoria
		"""
		Recupera il link diretto per il download del file dell'episodio.

		```
		return str # Link del file
		```
		"""
		pass #TODO: da completare

	def fileInfo(self) -> Dict[str,str]: # Opzionale
		"""
		Recupera le informazioni del file dell'episodio.

		```
		return {
		  "content_type": str, # Tipo del file, es. video/mp4
		  "total_bytes": int, # Byte totali del file
		  "last_modified": datetime, # Data e ora dell'ultimo aggiornamento effettuato all'episodio sul server
		  "server_name": str, # Nome del server
		  "server_id": int, # ID del server
		  "url": str # url dell'episodio
		} 
		```
		"""
		pass #TODO: da completare

	def download(self, title: Optional[str]=None, folder: str='', *, hook: Callable[[Dict], None]=lambda *args:None, opt: List[str]=[]) -> Optional[str]: # Obbligatoria
		"""
		Scarica l'episodio.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		- `hook`: Funzione che viene richiamata varie volte durante il download; la funzione riceve come argomento un dizionario con le seguenti chiavi: 
		  - `total_bytes`: Byte totali da scaricare.
		  - `downloaded_bytes`: Byte attualmente scaricati.
		  - `percentage`: Percentuale del progresso di download.
		  - `speed`: Velocità di download (byte/s)
		  - `elapsed`: Tempo trascorso dall'inizio del download.
		  - `eta`: Tempo stimato rimanente per fine del download.
		  - `status`: 'downloading' | 'finished' | 'aborted'
		  - `filename`: Nome del file in download.
		- `opt`: Lista per delle opzioni aggiuntive.
		  - `'abort'`: Ferma forzatamente il download.
		
		```
		return str # File scaricato
		```
		"""
		if title is None: title = self._defTitle
		else: title = self._sanitize(title)
		
		pass #TODO: da completare
```

1. Completare le varie funzioni (quelle segnate con `Opzionale` possono anche non essere completate), prendendo anche spunto dai vari server caricati nella cartella.

1. Aggiungi la linea `from .NuovoServer import NuovoServer` al file [servers/__init__.py](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/servers/__init__.py).

1. Modificare il file [episodio.py](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/episodio.py) aggiungendo il nome del server tra gli import ([Linea 11](https://github.com/MainKronos/AnimeWorld-API/blob/master/animeworld/episodio.py#L11)) e modificare la funzione [__setServer](https://github.com/MainKronos/AnimeWorld-API/blob/master/animeworld/episodio.py).

Se tutto funziona correttamente apri una richiesta di [pull](https://github.com/MainKronos/AnimeWorld-API/pulls).