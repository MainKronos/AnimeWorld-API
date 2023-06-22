"""
Modulo contenente la struttura a classe degli episodi.
"""
import httpx
from bs4 import BeautifulSoup
from typing import *
import time

from .utility import SES
from .exceptions import ServerNotSupported
from .servers import Server, AnimeWorld_Server, YouTube, Streamtape

class Episodio:
	"""
	Attributes:

	- `number`: Numero dell'episodio.
	- `links`: Lista dei server in cui è hostato l'episodio.

	Methods:

	- `download`: Scarica l'episodio dal primo server della lista links.
	"""

	def __init__(self, number: str, link: str, legacy: List[Dict] = []):
		"""
		- `number`: Numero dell'episodio.
		- `link`: Link dell'endpoint dell'episodio.
		- `legacy`: Lista di tutti i link dei server in cui sono hostati gli episodi.
		- `csrf_token`: Token per le chiamate api.
		"""
		self.number = number 
		"""Numero dell'episodio."""
		self.__link = link
		"""Link dell'endpoint dell'episodio."""
		self.__legacy = legacy
		"""Lista di tutti i link dei server in cui sono hostati gli episodi."""

	@property
	def links(self) -> List[Server]: # lista dei provider dove sono hostati gli ep
		"""
		Ottiene la lista dei server in cui è hostato l'episodio.

		```
		return [
		  Server, # Classe Server
		  ...
		]
		```
		"""
		tmp = [] # tutti i links
		res = SES.post(self.__link, timeout=(3, 27), follow_redirects=True)
		data = res.json()

		for provID in data["links"]:
			key = [x for x in data["links"][provID].keys() if x != 'server'][0]
			tmp.append({
				"id": int(provID),
				"name": data["links"][provID]["server"]["name"],
				"link": data["links"][provID][key]["link"]
			})
		
		for prov in self.__legacy:
			if str(prov['id']) in data["links"].keys(): continue

			tmp.append(prov)

		return self.__setServer(tmp, self.number)

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

		info = ""
		err = None
		for server in self.links:
			try:
				info = server.fileInfo()
			except ServerNotSupported:
				pass
			except httpx.HTTPError as exc:
				err = exc
			else:
				return info

		raise err

	def download(self, title: Optional[str]=None, folder: str='', *, hook: Callable[[Dict], None]=lambda *args:None, opt: List[str]=[]) -> Optional[str]: # Scarica l'episodio con il primo link nella lista
		"""
		Scarica l'episodio dal primo server funzionante della lista links.

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

		return self.__choiceBestServer().download(title,folder,hook=hook,opt=opt)

	# Private
	def __setServer(self, links: List[Dict], numero: str) -> List[Server]: # Per ogni link li posizioni nelle rispettive classi
		"""
		Costruisce la rispettiva classe Server per ogni link passato.

		- `links`: Dizionario ('id', 'name', 'link') contenente le informazioni del Server in cui è hostato l'episodio.
		- `numero`: Numero dell'episodio.

		```
		return [
		  Server, # Classe Server
		  ...
		]
		```
		"""
		ret: List[Server] = [] # lista dei server
		for prov in links:
			if prov["id"] == 4:
				ret.append(YouTube(prov["link"], prov["id"], prov["name"], numero))
			elif prov["id"] == 9:
				ret.append(AnimeWorld_Server(prov["link"], prov["id"], prov["name"], numero))
			elif prov["id"] == 8:
				ret.append(Streamtape(prov["link"], prov["id"], prov["name"], numero))
			else:
				ret.append(Server(prov["link"], prov["id"], prov["name"], numero))
		ret.sort(key=self.__sortServer)
		return ret

	# Private
	def __sortServer(self, elem):
		"""
		Ordina i server per importanza.
		"""
		if isinstance(elem, YouTube): return 0
		elif isinstance(elem, AnimeWorld_Server): return 1
		elif isinstance(elem, Streamtape): return 2
		else: return 4
	
	def __choiceBestServer(self) -> Server:
		"""
		Sceglie il server più veloce per il download dell'episodio.
		"""
		servers = self.links

		speed_test = [{
			"server": x,
			"bytes": -1
		} for x in servers]

		max_time = 0.5 # numero di secondi massimo

		for test in speed_test:
			try:
				start = time.perf_counter()
				link = test["server"].fileLink()
				if not link: continue
				with SES.stream("GET", link, timeout=0.9, follow_redirects=True) as r:
					for chunk in r.iter_bytes(chunk_size = 2048):
						if time.perf_counter() - start > max_time: break
						test["bytes"] += len(chunk)
			except (ServerNotSupported, httpx.HTTPError):
				continue
		
		speed_test = [x for x in speed_test if x["bytes"] != -1] # tolgo tutti i server che hanno generato un eccezione
		if len(speed_test) == 0: return servers[0] # ritorno al caso standard

		return max(speed_test, key=lambda x: x["bytes"])["server"] # restituisco il server che ha scaricato più byte in `max_time` secondi