"""
Modulo contenente la struttura a classe degli episodi.
"""
import requests
from bs4 import BeautifulSoup
from typing import *

from .globals import HDR, cookies
from .server import Server, AnimeWorld_Server, VVVVID, YouTube, Streamtape


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

		res = requests.post(self.__link, headers = HDR, cookies=cookies, timeout=(3, 27))
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

	def download(self, title: Optional[str]=None, folder: str='', show_progress: bool=True) -> Optional[str]: # Scarica l'episodio con il primo link nella lista
		"""
		Scarica l'episodio dal primo server della lista links.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		- `show_progress`: Mostra la barra di avanzamento.
		
		```
		return str # File scaricato
		```
		"""
		
		return self.links[0].download(title,folder)

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
		ret = [] # lista dei server
		for prov in links:
			if prov["id"] == 3: 
				ret.append(VVVVID(prov["link"], prov["id"], prov["name"], numero))
			elif prov["id"] == 4:
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
		if isinstance(elem, VVVVID): return 0
		elif isinstance(elem, YouTube): return 1
		elif isinstance(elem, AnimeWorld_Server): return 2
		elif isinstance(elem, Streamtape): return 3
		else: return 4