"""
Modulo per delle funzioni di utilità.
"""
import requests
from bs4 import BeautifulSoup
import inspect
from typing import *

from datetime import datetime
import time
import locale

from .globals import HDR, cookies
from .exceptions import DeprecatedLibrary


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
def find(keyword: str) -> List[Dict]:
	"""
	Ricerca un anime tramite le API interne di Animeworld.

	- `keyword`: Il nome dell'anime o una porzione di esso.

	```
	return [
	  {
	    "id": int, # ID interno di AnimeWorld
	    "name": str, # Nome dell'anime
	    "jtitle": str, # Nome giapponese (con caratteri latini)
	    "studio": str, # Studio dell'anime
	    "release": datetime, # Giorno, Mese e Anno della release dell'anime
	    "episodes": int, # Numero di episodi
	    "state": str, # Es. "0", "1", ...
	    "story": str, # Trama dell'anime
	    "categories": List[dict], # Es. [{"id": int, "name": str, "slug": str, "description": str}]
	    "image": str, # Link dell'immagine di copertina
	    "durationEpisodes": str, # Durata episodio
	    "link": str, # Link dell'anime
	    "createdAt": str, # Es. "2021-10-24T18:29:34.000Z"
	    "language": str, # Es. "jp
	    "year": str, # Anno di rilascio dell'anime
	    "dub": bool, # Se è doppiato o meno
	    "season": str, # Es. "winter"
	    "totViews": int, # Numero totale di visite alla pagina AnimeWolrd
	    "dayViews": int, # Numero giornaliero di visite alla pagina AnimeWolrd
	    "weekViews": int, # Numero settimanale di visite alla pagina AnimeWolrd
	    "monthViews": int, # Numero mensile di visite alla pagina AnimeWolrd
	    "malId": int, # ID di MyAnimeList dell'anime
	    "anilistId": int, # ID di AniList dell'anime
	    "mangaworldId": int, # ID di MangaWorld dell'anime
	    "malVote": float, # Valutazione di MyanimeList
	    "trailer": str # Link del trailer dell'anime
	  }
	]
	```
	"""

	locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")

	res = requests.get("https://www.animeworld.tv", headers = HDR)
	cookies.update(res.cookies.get_dict())
	soupeddata = BeautifulSoup(res.content, "html.parser")
	myHDR = {"csrf-token": soupeddata.find('meta', {'id': 'csrf-token'}).get('content')}


	res = requests.post("https://www.animeworld.tv/api/search/v2?", params = {"keyword": keyword} ,headers=myHDR, cookies=cookies)

	data = res.json()["animes"]
	data.sort(key=lambda a: a["dub"])

	return [
		{
		"id": elem["id"],
		"name": elem["name"],
		"jtitle": elem["jtitle"],
		"studio": elem["studio"],
		"release": datetime.strptime(elem["release"], "%d %B %Y"),
		"episodes": int(elem["state"]),
		"state": elem["state"],
		"story": elem["story"],
		"categories": elem["categories"],
		"image": elem["image"],
		"durationEpisodes": elem["durationEpisodes"],
		"link": f"https://www.animeworld.tv/play/{elem['link']}.{elem['identifier']}",
		"createdAt": elem["createdAt"],
		"language": elem["language"],
		"year": elem["year"],
		"dub": elem["dub"] != "0",
		"season": elem["season"],
		"totViews": elem["totViews"],
		"dayViews": elem["dayViews"],
		"weekViews": elem["weekViews"],
		"monthViews": elem["monthViews"],
		"malId": elem["malId"],
		"anilistId": elem["anilistId"],
		"mangaworldId": elem["mangaworldId"],
		"malVote": elem["malVote"],
		"trailer": elem["trailer"]
		}for elem in data
	]