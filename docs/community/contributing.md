# Contributing

## Server

Questa sezione spiega come aggiungere alla libreia la possibilità di scaricare un episodio da un'altro server non ancora supportato.

--8<-- "static/server.md"

Per aggiungere un nuovo server basta seguire questi passi:

1. Creare un file .py con il nome del server e metterlo nella cartella [servers](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/servers). (es `NuovoServer.py`)

1. Usa questo template per la classe del nuovo server: 
```py title="NuovoServer.py" linenums="1"
from .Server import *

class NuovoServer(Server):
	def fileLink(self): # Obbligatoria
		"""
		Recupera il link diretto per il download del file dell'episodio.

        Returns:
          Link diretto.

        Example:
          ```py
          return str # Link del file
          ```
		"""
		pass #TODO: da completare

	def fileInfo(self) -> Dict[str,str]: # Opzionale
		"""
        Recupera le informazioni del file dell'episodio.

        Returns:
          Informazioni file episodio.

        Example:
          ```py
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

        Args:
          title: Nome con cui verrà nominato il file scaricato.
          folder: Posizione in cui verrà spostato il file scaricato.

        Other parameters:
          hook: Funzione che viene richiamata varie volte durante il download; la funzione riceve come argomento un dizionario con le seguenti chiavi:\n 
            - `total_bytes`: Byte totali da scaricare.
            - `downloaded_bytes`: Byte attualmente scaricati.
            - `percentage`: Percentuale del progresso di download.
            - `speed`: Velocità di download (byte/s)
            - `elapsed`: Tempo trascorso dall'inizio del download.
            - `eta`: Tempo stimato rimanente per fine del download.
            - `status`: 'downloading' | 'finished' | 'aborted'
            - `filename`: Nome del file in download.

          opt: Lista per delle opzioni aggiuntive.\n
            - `'abort'`: Ferma forzatamente il download.
        
        Returns:
          Nome del file scaricato. 
        
        Raises:
          HardStoppedDownload: Il file in download è stato forzatamente interrotto.

        Example:
          ```py
          return str # File scaricato
          ```
        """
		if title is None: title = self._defTitle
		else: title = self._sanitize(title)
		
		pass

        #TODO: da completare, selezionare uno dei 2 metodi:
        # #NOTE: da usare se il file puó essere scaricato semplicemente con httpx:
        # return self._downloadIn(title,folder,hook=hook,opt=opt) 
        #
        # #NOTE: da usare se il file deve essere scaricato usando la libreria youtube_dl
        # return self._dowloadEx(title,folder,hook=hook,opt=opt) 
```

1. Completare le varie funzioni (quelle segnate con `Opzionale` possono anche non essere completate), prendendo anche spunto dai vari server caricati nella cartella.

1. Aggiungi la linea `from .NuovoServer import NuovoServer` al file [servers/__init__.py](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/servers/__init__.py).

1. Modificare il file [episodio.py](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/episodio.py) aggiungendo il nome del server tra gli import ([Linea 11](https://github.com/MainKronos/AnimeWorld-API/blob/master/animeworld/episodio.py#L11)) e modificare la funzione [__setServer](https://github.com/MainKronos/AnimeWorld-API/blob/master/animeworld/episodio.py).

Se tutto funziona correttamente apri una richiesta di [pull](https://github.com/MainKronos/AnimeWorld-API/pulls).