"""
AnimeWorld-API
"""
import json
import requests
from bs4 import BeautifulSoup
import youtube_dl
import re
import inspect
import time
import os
from typing import *


HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
cookies = {}
## Function ##########################################

	
def HealthCheck(fun):
	"""
	Controlla se la libreria è deprecata
	"""
	def wrapper(*args, **kwargs):
		try:
			return fun(*args, **kwargs)
		except AttributeError:
			frame = inspect.trace()[-1]
			funName = frame[3]
			errLine = frame[2]
			raise DeprecatedLibrary(funName, errLine)
	return wrapper

@HealthCheck
def find(keyword: str) -> Optional[Dict]:
	"""
	Ricerca un anime tramite le API interne di Animeworld.

	- `keyword`: Il nome dell'anime o una porzione di esso.

	```
	return {
	  name: str, # Nome dell'anime trovato
	  link: str # Link dell'anime trovato
	}
	```
	"""
	res = requests.get("https://www.animeworld.tv", headers = HDR)
	cookies.update(res.cookies.get_dict())
	soupeddata = BeautifulSoup(res.content, "html.parser")
	myHDR = {"csrf-token": soupeddata.find('meta', {'id': 'csrf-token'}).get('content')}


	res = requests.post("https://www.animeworld.tv/api/search/v2?", params = {"keyword": keyword} ,headers=myHDR, cookies=cookies)

	data = res.json()["animes"]
	data.sort(key=lambda a: a["dub"])

	# with open("index.html", 'w') as f:
	# 	json.dump(data, f, indent='\t')


	if len(data) == 0:
		return None
	else:
		return {
			"name": data[0]["name"],
			"link": f"https://www.animeworld.tv/play/{data[0]['link']}.{data[0]['identifier']}"
		}


########################################################

### Server ###

class Server:
	"""
	Attributes:

	- `link`: Link del server in cui è hostato l'episodio.
	- `Nid`: ID del server.
	- `name`: Nome del server.
	- `number`: Numero dell'episodio.

	Methods:

	- `download`: Scarica l'episodio.
	"""

	def __init__(self, link: str, Nid: int, name: str, number: str):
		"""
		- `link`: Link del server in cui è hostato l'episodio.
		- `Nid`: ID del server.
		- `name`: Nome del server.
		- `number`: Numero dell'episodio.
		"""

		self.link = link
		"""Link del server in cui è hostato l'episodio."""
		self.Nid = Nid
		"""ID del server."""
		self.name = name
		"""Nome del server."""
		self.number = number
		"""Numero dell'episodio."""

		self._HDR = HDR # Protected 
		self._defTitle = f"{self.number} - {self.name}" # nome del file provvisorio

	def _sanitize(self, title: str) -> str: # Toglie i caratteri illegali per i file
		"""
		Rimuove i caratteri illegali per il nome del file.

		- `title`: Nome del file.

		```
		return str # title sanitizzato
		```
		"""
		illegal = ['#','%','&','{','}', '\\','<','>','*','?','/','$','!',"'",'"',':','@','+','`','|','=']
		for x in illegal:
			title = title.replace(x, '')
		return title

	def download(self, title: Optional[str]=None, folder: str='') -> NoReturn:
		"""
		Scarica l'episodio.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		
		"""
		raise ServerNotSupported(self.name)

	# Protected
	def _downloadIn(self, title: str, folder: str) -> bool: # Scarica l'episodio
		"""
		Scarica il file utilizzando requests.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.

		```
		return bool # File scaricato
		```
		"""
		with requests.get(self._getFileLink(), headers = self._HDR, stream = True) as r:
			r.raise_for_status()
			with open(f"{os.path.join(folder,title)}.mp4", 'wb') as f:
				for chunk in r.iter_content(chunk_size = 1024*1024):
					if chunk: 
						f.write(chunk)
				else:
					return True # Se il file è stato scaricato correttamente
		return False # Se è accaduto qualche imprevisto

	# Protected
	def _dowloadEx(self, title: str, folder: str):
		"""
		Scarica il file utilizzando yutube_dl.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.

		```
		return bool # File scaricato
		```
		"""
		class MyLogger(object):
			def debug(self, msg):
				pass
			def warning(self, msg):
				pass
			def error(self, msg):
				print(msg)
				return False
		def my_hook(d):
			if d['status'] == 'finished':
				return True

		ydl_opts = {
			'outtmpl': f"{os.path.join(folder,title)}.%(ext)s",
			'logger': MyLogger(),
			'progress_hooks': [my_hook],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([self._getFileLink()])
			return True


class AnimeWorld_Server(Server):
	# Protected
	@HealthCheck
	def _getFileLink(self):

		return self.link.replace('download-file.php?id=', '')

	def download(self, title: Optional[str]=None, folder: str='') -> bool:
		"""
		Scarica l'episodio.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		
		```
		return bool # File scaricato
		```
		"""
		if title is None: title = self._defTitle
		else: title = self._sanitize(title)
		return self._downloadIn(title,folder)

class VVVVID(Server):
	# Protected
	@HealthCheck
	def _getFileLink(self):
		anime_id = self.link.split("/")[-1]
		external_link = "https://www.animeworld.tv/api/episode/serverPlayerAnimeWorld?id={}".format(anime_id)
		"https://www.animeworld.tv/api/episode/serverPlayerAnimeWorld?id=vKmnNB"

		sb_get = requests.get(self.link, headers = self._HDR, cookies=cookies)
		sb_get.raise_for_status()

		sb_get = requests.get(external_link, headers = self._HDR, cookies=cookies)
		soupeddata = BeautifulSoup(sb_get.content, "html.parser")
		sb_get.raise_for_status()
					
		raw = soupeddata.find("a", { "class" : "VVVVID-link" })
		return raw.get("href")

	def download(self, title: Optional[str]=None, folder: str='') -> bool:
		"""
		Scarica l'episodio.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		
		```
		return bool # File scaricato
		```
		"""
		if title is None: title = self._defTitle
		else: title = self._sanitize(title)
		return self._dowloadEx(title,folder)
		

class YouTube(Server):
	# Protected
	@HealthCheck
	def _getFileLink(self):
		anime_id = self.link.split("/")[-1]
		external_link = "https://www.animeworld.tv/api/episode/serverPlayerAnimeWorld?id={}".format(anime_id)

		sb_get = requests.get(self.link, headers = self._HDR, cookies=cookies)
		sb_get.raise_for_status()

		sb_get = requests.get(external_link, headers = self._HDR, cookies=cookies)
		soupeddata = BeautifulSoup(sb_get.content, "html.parser")
		sb_get.raise_for_status()

		yutubelink_raw = re.search(r'"(https:\/\/www\.youtube\.com\/embed\/.+)"\);', soupeddata.prettify()).group(1)

		print( yutubelink_raw.replace('embed/', 'watch?v='))

		return yutubelink_raw.replace('embed/', 'watch?v=')

	def download(self, title: Optional[str]=None, folder: str='') -> bool:
		"""
		Scarica l'episodio.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		
		```
		return bool # File scaricato
		```
		"""
		if title is None: title = self._defTitle
		else: title = self._sanitize(title)
		return self._dowloadEx(title,folder)

class Streamtape(Server):
	# Protected
	@HealthCheck
	def _getFileLink(self):

		sb_get = requests.get(self.link, headers = self._HDR, cookies=cookies, allow_redirects=False)

		with open('inde.html', 'wb') as f:
			f.write(sb_get.content)

		if sb_get.status_code == 200:
			soupeddata = BeautifulSoup(sb_get.content, "html.parser")

			raw_link = re.search(r"document\.getElementById\('ideoooolink'\)\.innerHTML = (\".*'\))", soupeddata.prettify()).group(1)

			raw_link = raw_link.replace('"', '').replace("'", "").replace('+', '')

			raw_link_part2 = re.search(r"\((.*?)\)", raw_link).group(1)[4:]
			raw_link_part1 = re.sub(r"\(.*?\)",'', raw_link)

			mp4_link = 'http:/' + (raw_link_part1 + raw_link_part2).replace(' ', '')

			return mp4_link

	def download(self, title: Optional[str]=None, folder: str='') -> bool:
		"""
		Scarica l'episodio.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		
		```
		return bool # File scaricato
		```
		"""
		if title is None: title = self._defTitle
		else: title = self._sanitize(title)
		return self._downloadIn(title,folder)

## Class ###############################################

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

	def download(self, title: Optional[str]=None, folder: str='') -> Union[bool, NoReturn]: # Scarica l'episodio con il primo link nella lista
		"""
		Scarica l'episodio dal primo server della lista links.

		- `title`: Nome con cui verrà nominato il file scaricato.
		- `folder`: Posizione in cui verrà spostato il file scaricato.
		
		```
		return bool # File scaricato
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

########################################################


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

		for ep in raw:
			epNum =ep
			epID = raw[ep]["episodeId"]

			legacy_links = []


			for provID in provLegacy:
				legacy_links.append({
					"id": int(provID),
					"name": provLegacy[provID]["name"],
					"link": "https://www.animeworld.tv" + provLegacy[provID]["soup"].find('a', {'data-episode-num': ep}).get("href")
				})


			ep = Episodio(epNum, f"https://www.animeworld.tv/api/download/{epID}", legacy_links)
			eps.append(ep)

		return eps

## ERRORS #############################################

class ServerNotSupported(Exception):
	"""Il server da dove si tenta di scaricare l'episodio non è supportato."""
	def __init__(self, server):
		self.server = server
		self.message = f"Il server {server} non è supportato."
		super().__init__(self.message)

class AnimeNotAvailable(Exception):
	"""L'anime non è ancora disponibile."""
	def __init__(self, animeName=''):
		self.anime = animeName
		self.message = f"L'anime '{animeName}' non è acora disponibile."
		super().__init__(self.message)

class Error404(Exception):
	"""Il link porta ad una pagina inesistente."""
	def __init__(self, link):
		self.link = link
		self.message = f"Il link '{link}' porta ad una pagina inesistente."
		super().__init__(self.message)

class DeprecatedLibrary(Exception):
	"""Libreria deprecata a causa di un cambiamento della struttura del sito."""
	def __init__(self, funName, line):
		self.funName = funName
		self.line = line
		self.message = f"Il sito è cambiato, di conseguenza la libreria è DEPRECATA. -> [{funName} - {line}]"
		super().__init__(self.message)

