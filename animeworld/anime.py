"""
Modulo contenente la struttura a classe dell'anime.
"""
import requests
from bs4 import BeautifulSoup
import re
import time
from typing import *

from .globals import HDR, cookies
from .utility import HealthCheck
from .exceptions import Error404, AnimeNotAvailable
from .episodio import Episodio

class Anime:
	"""
	Attributes:

	- `link`: Link dell'anime.
	- `html`: Pagina web di Animeworld dell'anime.

	Methods:

	- `getName`: Ottiene il nome dell'anime.
	- `getTrama`: Ottiene la trama dell'anime.
	- `getInfo`: Ottiene le informazioni dell'anime.
	- `getEpisodes`: Ottiene tutti gli episodi dell'anime.
	"""



	def __init__(self, link: str):
		"""
		- `link`: Link dell'anime.
		"""
		self.link = link
		self.__fixCookie()
		self.html = self.__getHTML().content
		self.__check404()

	# Private
	def __fixCookie(self):
		"""
		Aggiorna il cookie `AWCookieVerify`.
		"""
		try:
			soupeddata = BeautifulSoup(self.__getHTML().content, "html.parser")

			cookies['AWCookieVerify'] = re.search(r'document\.cookie="AWCookieVerify=(.+) ;', soupeddata.prettify()).group(1)
			
		except AttributeError:
			pass

	# Private
	def __getHTML(self) -> requests.Response:
		"""
		Ottiene la pagina web di Animeworld dell'anime e aggiorna i cookies.
		
		```
		return Response # Risposta GET
		```
		"""
		r = None
		while True:
			try:
				r = requests.get(self.link, headers = HDR, cookies=cookies, timeout=(3, 27), allow_redirects=True)

				cookies.update(r.cookies.get_dict())

				if len(list(filter(re.compile(r'30[^2]').search, [str(x.status_code) for x in r.history]))): # se c'è un redirect strano
					continue

			except requests.exceptions.ReadTimeout:
				time.sleep(1) # errore
				
			else:
				break
		r.raise_for_status()
		return r
	
	# Private
	def __check404(self):
		"""
		Controlla se la pagina è una pagina 404.
		"""
		if self.html.decode("utf-8").find('Errore 404') != -1: raise Error404(self.link)

	# Private
	@HealthCheck
	def __getServer(self) -> Dict[int, Dict[str, str]]:
		"""
		Ottiene tutti i server in cui sono hostati gli episodi.

		```
		return {
		  int: { # ID del server
		    name: str # Nome del server
		  },
		  ...
		}
		```
		"""
		soupeddata = BeautifulSoup(self.html, "html.parser")
		block = soupeddata.find("span", { "class" : "servers-tabs" })

		if block == None: raise AnimeNotAvailable(self.getName())

		providers = block.find_all("span", { "class" : "server-tab" })
		return {
			int(x["data-name"]): {
				"name": x.get_text()
			} 
			for x in providers
		}

	@HealthCheck
	def getTrama(self) -> str:
		"""
		Ottiene la trama dell'anime.

		```
		return str # Trama dell'anime
		```
		"""
		soupeddata = BeautifulSoup(self.html, "html.parser")
		return soupeddata.find("div", { "class" : "desc" }).get_text()

	@HealthCheck
	def getInfo(self) -> Dict[str, str]:
		"""
		Ottiene le informazioni dell'anime.

		```
		return {
		  'Categoria': str,
		  'Audio': str,
		  'Data di Uscita': str,
		  'Stagione': str,
		  'Studio': str,
		  'Genere': List[str],
		  'Voto': str,
		  'Durata': str,
		  'Episodi': str,
		  'Stato': str,
		  'Visualizzazioni': str
		}
		```
		"""
		soupeddata = BeautifulSoup(self.html, "html.parser")
		block = soupeddata.find("div", { "class" : "info" }).find("div", { "class" : "row" })

		tName = [x.get_text().replace(':', '') for x in block.find_all("dt")]
		tInfo = []
		for x in block.find_all("dd"):
			txt = x.get_text()
			if len(txt.split(',')) > 1:
				tInfo.append([x.strip() for x in txt.split(',')])
			else:	
				tInfo.append(txt.strip())

		return dict(zip(tName, tInfo))

	@HealthCheck
	def getName(self) -> str: # Nome dell'anime
		"""
		Ottiene il nome dell'anime.

		```
		return str # Nome dell'anime
		```
		"""
		soupeddata = BeautifulSoup(self.html, "html.parser")
		return soupeddata.find("h1", { "id" : "anime-title" }).get_text()

	#############

	@HealthCheck
	def getEpisodes(self) -> List[Episodio]: # Ritorna una lista di Episodi
		"""
		Ottiene tutti gli episodi dell'anime.

		```
		return [
		  Episodio, # Classe Episodio
		  ...
		]
		```
		"""
		soupeddata = BeautifulSoup(self.html, "html.parser")

		self.link = "https://www.animeworld.tv" + soupeddata.select_one('li.episode > a').get('href')

		soupeddata = BeautifulSoup(self.__getHTML().content, "html.parser")

		HDR.update({"csrf-token": soupeddata.find('meta', {'id': 'csrf-token'}).get('content')})

		raw = {} # dati in formato semi-grezzo
		eps = [] # Lista di Episodio()


		provLegacy = self.__getServer() # vecchio sistema di cattura server

		raw = {}
		for liElem in soupeddata.find_all("li", {"class": "episode"}):
			aElem = liElem.find('a')
			raw[aElem.get('data-episode-num')] = {
				"episodeId": aElem.get('data-episode-id')
			}

		for provID in provLegacy:
			provLegacy[provID]["soup"] = soupeddata.find("div", {"class": "server", "data-name": str(provID)})

		for epNum in raw:
			epID = raw[epNum]["episodeId"]
			legacy_links = []

			for provID in provLegacy:
				soup_link = provLegacy[provID]["soup"].find('a', {'data-episode-num': epNum})

				if soup_link:
					legacy_links.append({
						"id": int(provID),
						"name": provLegacy[provID]["name"],
						"link": "https://www.animeworld.tv" + soup_link.get("href")
					})


			eps.append(Episodio(epNum, f"https://www.animeworld.tv/api/download/{epID}", legacy_links))

		return eps