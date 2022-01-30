"""
Modulo contenente le strutture a classi di tutti i server che hostano gli episodi di animewolrd.
"""
import requests
from bs4 import BeautifulSoup
import youtube_dl
import re
import os
from typing import *

from .globals import HDR, cookies
from .utility import HealthCheck
from .exceptions import ServerNotSupported


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