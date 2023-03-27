from bs4 import BeautifulSoup
import re

from .Server import *
from ..utility import HealthCheck

class YouTube(Server):
	@HealthCheck
	def fileLink(self) -> str:
		"""
		Recupera il link diretto per il download del file dell'episodio.

		```
		return str # Link del file
		```
		"""
		
		anime_id = self.link.split("/")[-1]
		external_link = "https://www.animeworld.tv/api/episode/serverPlayerAnimeWorld?id={}".format(anime_id)

		sb_get = SES.get(self.link)
		sb_get.raise_for_status()

		sb_get = SES.get(external_link)
		soupeddata = BeautifulSoup(sb_get.content, "html.parser")
		sb_get.raise_for_status()

		yutubelink_raw = re.search(r'"(https:\/\/www\.youtube\.com\/embed\/.+)"\);', soupeddata.prettify()).group(1)

		return yutubelink_raw.replace('embed/', 'watch?v=')

	def fileInfo(self) -> Dict[str,str]:
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

		return self._fileInfoEx()

	def download(self, title: Optional[str]=None, folder: str='', *, hook: Callable[[Dict], None]=lambda *args:None, opt: List[str]=[]) -> Optional[str]:
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
		return self._dowloadEx(title,folder,hook=hook,opt=opt)