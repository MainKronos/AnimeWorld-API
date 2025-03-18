"""
Modulo per delle funzioni di utilità.
"""
import os

import httpx
from bs4 import BeautifulSoup
import inspect
from typing import *
import re

from .exceptions import DeprecatedLibrary

base_path = os.getenv('BASE_PATH', 'https://www.animeworld.so')

class MySession(httpx.Client):
    """
    Sessione httpx.
    """
    def __init__(self) -> None:
        super().__init__(http2=True)
        self.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
        self.fixCookie()
    
    def fixCookie(self):
        """Aggiunge il csrf_token all'headers."""

        csrf_token = re.compile(br'<meta.*?id="csrf-token"\s*?content="(.*?)">')
        cookie = re.compile(br'document\.cookie\s*?=\s*?"(.+?)=(.+?)(\s*?;\s*?path=.+?)?"\s*?;')
        for _ in range(2): # numero di tentativi
            res = self.get(base_path, follow_redirects=True)

            m = cookie.search(res.content)
            if m:
                self.cookies.update({m.group(1).decode('utf-8'): m.group(2).decode('utf-8')})
                continue
            
            m = csrf_token.search(res.content)
            if m:
                self.headers.update({'csrf-token': m.group(1).decode('utf-8')})
                break


def HealthCheck(fun):
    """
    Controlla se la libreria è deprecata
    """
    def wrapper(*args, **kwargs):
        try:
            attempt = False # tentativo utilizzato
            while True:
                try:
                    return fun(*args, **kwargs)
                except Exception as e:
                    if not attempt:
                        SES.fixCookie()
                    else:
                        raise e
                    attempt = True

        except AttributeError:
            frame = inspect.trace()[-1]
            funName = frame[3]
            errLine = frame[2]
            filename = frame[1]
            raise DeprecatedLibrary(filename, funName, errLine)
    return wrapper

@HealthCheck
def find(keyword: str) -> List[Dict]:
    """
    Ricerca un anime tramite le API interne di Animeworld.

    Args:
      keyword: Il nome dell'anime o una porzione di esso.

    Returns:
      Informazioni riguardanti l'anime.
    
    Raises:
      DeprecatedLibrary: Cambiamento del sito Animeworld.

    Example:
      ```py
      [
        {
          "id": int, # ID interno di AnimeWorld
          "name": str, # Nome dell'anime
          "jtitle": str, # Nome giapponese (con caratteri latini)
          "studio": str, # Studio dell'anime
          "release": str | None, # Giorno, Mese e Anno della release dell'anime. Se non disponibile ("??" al posto della data), ritorna None.
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

    res = SES.post(f"{base_path}/api/search/v2?", params = {"keyword": keyword}, follow_redirects=True)

    data = res.json()
    if "error" in data: return []
    data = data["animes"]

    for elem in data:
        for k in elem:
            if elem[k] == "??":
                elem[k] = None

    data.sort(key=lambda a: a["dub"])

    return [
        {
        "id": elem["id"],
        "name": elem["name"],
        "jtitle": elem["jtitle"],
        "studio": elem["studio"],
        "release": elem["release"],
        "episodes": int(elem["episodes"]) if elem["episodes"] is not None else None,
        "state": elem["state"],
        "story": elem["story"],
        "categories": elem["categories"],
        "image": elem["image"],
        "durationEpisodes": elem["durationEpisodes"],
        "link": f"{base_path}/play/{elem['link']}.{elem['identifier']}" if elem['link'] is not None or elem['identifier'] is not None else None,
        "createdAt": elem["createdAt"],
        "language": elem["language"],
        "year": elem["year"],
        "dub": elem["dub"] != "0" if elem["dub"] is not None else None,
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

SES = MySession() # sessione contenente Cookie e headers
"Sessione httpx."
