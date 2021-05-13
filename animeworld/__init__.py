import requests
from bs4 import BeautifulSoup
import youtube_dl
import re
import inspect

HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
cookies = {'AWCookieVerify': None}


## Function ##########################################

def find(animeName): # Deprecata
	ret = {}

	search = "https://www.animeworld.tv/search?keyword={}".format(animeName.replace(" ", "%20"))
	sb_get = requests.get(search, headers = HDR)
	soupeddata = BeautifulSoup(sb_get.content, "html.parser")

	page_result = soupeddata.find("div", { "class" : "film-list" }).find_all("a", { "class" : "name" })
	for x in page_result:
		ret[x.get_text()] = f"https://www.animeworld.tv{x.get('href')}"

	return ret
	
def HealthCheck(fun): # Controlla se la libreria è deprecata
	def wrapper(*args, **kwargs):
		try:
			return fun(*args, **kwargs)
		except AttributeError:
			frame = inspect.trace()[-1]
			funName = frame[3]
			errLine = frame[2]
			raise DeprecatedLibrary(funName, errLine)
	return wrapper

########################################################

## Class ###############################################

class Anime:
	# mapped = {
	# 	2:"DoodStream",
	# 	3:"VVVVID",
	# 	4:"YouTube",
	# 	8:"Streamtape",
	# 	9:"AnimeWorld Server",
	# 	10:"Beta Server",
	# 	11:"OkStream",
	# 	15:"NinjaStream",
	# 	17:"Userload",
	# 	18:"VUP"
	# }

	def __init__(self, link):
		self.link = link
		self.__fixCookie()
		self.html = self.__getHTML().content
		# self.server = self.__getServer()
		# self.nome = self.getName()
		# self.trama = self.getTrama()
		# self.info = self.getInfo()

	# Private
	def __fixCookie(self):
		try:
			res = self.__getHTML()
			cookies['AWCookieVerify'] = re.search(r'document\.cookie="AWCookieVerify=(.+) ;', res.text).group(1)
		except AttributeError:
			pass

	### INFO ####

	# Private
	def __getHTML(self):
		r = requests.get(self.link, headers = HDR, cookies=cookies)
		r.raise_for_status()
		return r

	# Private
	@HealthCheck
	def __getServer(self): # Provider dove sono hostati gli episodi
		soupeddata = BeautifulSoup(self.html, "html.parser")
		block = soupeddata.find("span", { "class" : "servers-tabs" })

		if block == None: raise AnimeNotAvailable(self.getName())

		providers = block.find_all("span", { "class" : "server-tab" })
		data = {int(x["data-name"]):x.get_text() for x in providers}
		return data

	@HealthCheck
	def getTrama(self): # Trama dell'anime 
		soupeddata = BeautifulSoup(self.html, "html.parser")
		return soupeddata.find("div", { "class" : "desc" }).get_text()

	@HealthCheck
	def getInfo(self): # Informazioni dell'anime
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
	def getName(self): # Nome dell'anime
		soupeddata = BeautifulSoup(self.html, "html.parser")
		return soupeddata.find("h1", { "id" : "anime-title" }).get_text()

	#############

	@HealthCheck
	def getEpisodes(self): # Ritorna una lista di Episodi
		raw = {} # dati in formato semi-grezzo
		server = self.__getServer()
		soupeddata = BeautifulSoup(self.html, "html.parser")
		for idProvider in server:
			epBox = soupeddata.find("div", { "class" : "server", "data-name": str(idProvider)})
			ep_links = epBox.find_all("a")
			for x in ep_links:
				if x.get_text() not in raw.keys(): raw[x.get_text()] = {}
				raw[x.get_text()][idProvider] = "https://www.animeworld.tv" + x.get("href")

		eps = [] # Lista di Episodio()
		for episode in raw:
			links = self.__setServer(server, raw[episode], episode)
			ep = Episodio(episode, links)
			eps.append(ep)

		return eps

	# Private
	def __setServer(self, mapp, links, numero): # Per ogni link li posizioni nelle rispettive classi
		ret = [] # lista dei server
		for link in links:
			if link == 3: 
				ret.append(VVVVID(links[link], link, mapp[link], numero))
			elif link == 4:
				ret.append(YouTube(links[link], link, mapp[link], numero))
			elif link == 9:
				ret.append(AnimeWorld_Server(links[link], link, mapp[link], numero))
			elif link == 8:
				ret.append(Streamtape(links[link], link, mapp[link], numero))
			else:
				ret.append(Server(links[link], link, mapp[link], numero))
		ret.sort(key=self.__sortServer)
		return ret

	# Private
	def __sortServer(self, elem): # Ordina i server per importanza
		if isinstance(elem, VVVVID): return 0
		elif isinstance(elem, YouTube): return 1
		elif isinstance(elem, AnimeWorld_Server): return 2
		elif isinstance(elem, Streamtape): return 3
		else: return 4



class Episodio:
	def __init__(self, number, links):
		self.number = number # Numero dell'episodio
		self.links = links # Array di Server()

	def download(self, title=None): # Scarica l'episodio con il primo link nella lista
		return self.links[0].download(title)

### Server ###

class Server:
	def __init__(self, link, Nid, name, numero):
		self.link = link # Link del server dove è hostato l'episodio (str)
		self.Nid = Nid # Id del server (int)
		self.name = name # Nome del server
		self.number = numero # Numero dell'episodio
		self._HDR = HDR # Protected 
		self._defTitle = f"{self.number} - {self.name}"

	def sanitize(self, title): # Toglie i caratteri illegali per i file
		illegal = ['#','%','&','{','}', '\\','<','>','*','?','/','$','!',"'",'"',':','@','+','`','|','=']
		for x in illegal:
			title = title.replace(x, '')
		return title

	def download(self, title=None):
		raise ServerNotSupported(self.name)

	# Protected
	def _downloadIn(self, title): # Scarica l'episodio
		with requests.get(self._getFileLink(), headers = self._HDR, stream = True) as r:
			r.raise_for_status()
			with open(f"{title}.mp4", 'wb') as f:
				for chunk in r.iter_content(chunk_size = 1024*1024):
					if chunk: 
						f.write(chunk)
				else:
					return True # Se il file è stato scaricato correttamente
		return False # Se è accaduto qualche imprevisto

	# Protected
	def _dowloadEx(self, title): # Scarica l'episodio con l'utilizzo della libreria yutube_dl
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
			'outtmpl': title+'.%(ext)s',
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
		anime_id = self.link.split("/")[-1]
		video_link = "https://www.animeworld.tv/api/episode/serverPlayerAnimeWorld?id={}".format(anime_id)

		sb_get = requests.get(video_link, headers = self._HDR, cookies=cookies)
		sb_get.raise_for_status()

		soupeddata = BeautifulSoup(sb_get.content, "html.parser")
		raw_ep = soupeddata.find("video", { "id" : "video-player" }).find("source", { "type" : "video/mp4" })

		self._HDR["Referer"] = video_link
		return raw_ep.get("src")

	def download(self, title=None):
		if title is None: title = self._defTitle
		else: title = self.sanitize(title)
		return self._downloadIn(title)

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

	def download(self, title=None):
		if title is None: title = self._defTitle
		else: title = self.sanitize(title)
		return self._dowloadEx(title)
		

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
		return yutubelink_raw.replace('embed/', 'watch?v=')

	def download(self, title=None):
		if title is None: title = self._defTitle
		else: title = self.sanitize(title)
		return self._dowloadEx(title)

class Streamtape(Server):
	# Protected
	@HealthCheck
	def _getFileLink(self):
		sb_get = requests.get(self.link, headers = self._HDR, cookies=cookies)
		if sb_get.status_code == 200:
			soupeddata = BeautifulSoup(sb_get.content, "html.parser")
			site_link = soupeddata.find("div", { "id" : "external-downloads" }).find("a", { "class" : "btn-streamtape" }).get("href")
			sb_get = requests.get(site_link, headers = self._HDR, cookies=cookies)
			if sb_get.status_code == 200:

				soupeddata = BeautifulSoup(sb_get.content, "html.parser")

				mp4_link = "https://" + re.search(r"document\.getElementById\(\'vid\'\+\'eolink\'\)\.innerHTML = \"\/\/(.+)\'\;", soupeddata.prettify()).group(1)
				return mp4_link.replace(" ", "").replace("+", "").replace("\'", "").replace("\"", "")

	def download(self, title=None):
		if title is None: title = self._defTitle
		else: title = self.sanitize(title)
		return self._downloadIn(title)

########################################################

## ERRORS #############################################

class ServerNotSupported(Exception): # Il server da dove si tenta di scaricare l'episodio non è supportato
	def __init__(self, server):
		self.server = server
		self.message = f"Il server {server} non è supportato."
		super().__init__(self.message)

class AnimeNotAvailable(Exception): # L'anime non è ancora disponibile
	def __init__(self, animeName=''):
		self.anime = animeName
		self.message = f"L'anime '{animeName}' non è acora disponibile."
		super().__init__(self.message)

class DeprecatedLibrary(Exception):
	def __init__(self, funName, line):
		self.funName = funName
		self.line = line
		self.message = f"Il sito è cambiato, di conseguenza la libreria è DEPRECATA. -> [{funName} - {line}]"
		super().__init__(self.message)
