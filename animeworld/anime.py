"""
Modulo contenente la struttura a classe dell'anime.
"""
import httpx
from bs4 import BeautifulSoup
import re
import time
from typing import *

from .utility import HealthCheck, SES
from .exceptions import Error404, AnimeNotAvailable
from .episodio import Episodio

class Anime:
    """
    Attributes:
      link: Link dell'anime.
      html: Pagina web di Animeworld dell'anime.
    """

    def __init__(self, link: str):
        """		
        Args:
          link: Link dell'anime.
        
        Raises:
          DeprecatedLibrary: Cambiamento del sito Animeworld.
          Error404: È una pagina 404.
        """

        self.link:str = httpx.URL(link).path
        self.html:bytes = self.__getHTML().content
        self.__check404()

    # Private
    def __getHTML(self) -> httpx.Response:
        """
        Ottiene la pagina web di Animeworld dell'anime e aggiorna i cookies.

        Returns:
          La risposta di requests.

        Raises:
          DeprecatedLibrary: Cambiamento del sito Animeworld.
        
        Example:
          ```py
          return Response # Risposta GET
          ```
        """
        r = None
        retry = 0
        while True:
            try:
                r = SES.get(self.link, timeout=(3, 27), follow_redirects=True)

            except httpx.ReadTimeout as e:
                if retry <= 2:
                    retry +=1
                    time.sleep(1) # errore
                else:
                    raise e
                
            else:
                break
        r.raise_for_status()
        return r
    
    # Private
    def __check404(self):
        """
        Controlla se la pagina è una pagina 404.

        Raises:
          Error404: È una pagina 404.
        """
        if self.html.decode("utf-8").find('Errore 404') != -1: raise Error404(self.link)

    # Private
    @HealthCheck
    def __getServer(self) -> List[Dict[str, str]]:
        """
        Ottiene tutti i server in cui sono hostati gli episodi.

        Raises:
          DeprecatedLibrary: Cambiamento del sito Animeworld.
          AnimeNotAvailable: L'anime non è ancora disponibile.

        Example:
          ```
          return [
            {
                name: str # Nome del server
                id: str # ID del server
            ],
            ...
          }
          ```
        """
        soupeddata = BeautifulSoup(self.html, "html.parser")
        block = soupeddata.find("span", { "class" : "servers-tabs" })

        if block == None: raise AnimeNotAvailable(self.getName())

        providers = block.find_all("span", { "class" : "server-tab" })
        return [
            {
                "name": x.get_text(),
                "id": x["data-name"]
            } 
            for x in providers
        ]

    @HealthCheck
    def getTrama(self) -> str:
        """
        Ottiene la trama dell'anime.

        Returns:
          La trama dell'anime.
        
        Raises:
          DeprecatedLibrary: Cambiamento del sito Animeworld.
        
        Example:
          ```py
          return str # Trama anime.
          ```
        """
        soupeddata = BeautifulSoup(self.html, "html.parser")
        return soupeddata.find("div", { "class" : "desc" }).get_text()

    @HealthCheck
    def getCover(self) -> str:
        """
        Ottiene l'url dell'immagine di copertina dell'anime.

        Returns:
          Url dell'immagine di copertina dell'anime.
        
        Raises:
          DeprecatedLibrary: Cambiamento del sito Animeworld.
        
        Example:
          ```py
          return str # Url dell'immagine di copertina dell'anime
          ```
        """
        soupeddata = BeautifulSoup(self.html, "html.parser")
        return soupeddata.find("div", { "id" : "thumbnail-watch" }).find("img")["src"]

    @HealthCheck
    def getInfo(self) -> Dict[str, str]:
        """
        Ottiene le informazioni dell'anime.

        Returns:
          Informazioni anime.
        
        Raises:
          DeprecatedLibrary: Cambiamento del sito Animeworld.
        
        Example:
          ```py
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

        Returns:
          Nome anime.
        
        Raises:
          DeprecatedLibrary: Cambiamento del sito Animeworld.

        Example:
          ```py
          return str # Nome dell'anime
          ```
        """
        soupeddata = BeautifulSoup(self.html, "html.parser")
        return soupeddata.find("h1", { "id" : "anime-title" }).get_text()

    #############

    @HealthCheck
    def getEpisodes(self, nums: Union[List[int], List[str]] = None) -> List[Episodio]: # Ritorna una lista di Episodi
        """
        Ottiene tutti gli episodi dell'anime.

        Args:
          nums: I numeri degli episodi da ottenere

        Note:
          Se `nums` è `None` o `[]` allora il metodo restituisce tutti gli episodi dell'anime.

        Returns:
          Lista di oggetti Episodio.
        
        Raises:
          AnimeNotAvailable: L'anime non è ancora disponibile.
          DeprecatedLibrary: Cambiamento del sito Animeworld.
          
        Example:
          ```py
          return [
            Episodio, # Classe Episodio
            ...
          ]
          ```
        """

        # Controllo se viene passata una lista di episodi da filtrare
        if nums: nums = list(map(str, nums))

        soupeddata = BeautifulSoup(self.html.decode('utf-8', 'ignore'), "html.parser")

        a_link = soupeddata.select_one('li.episode > a')
        if a_link is None: raise AnimeNotAvailable(self.getName())

        self.link = str(SES.build_url(a_link.get('href')))

        server_list = self.__getServer()

        raw_eps = {}
        for server_info in server_list:
            server_id = int(server_info['id'])
            server_name = server_info['name']

            server_soup = soupeddata.select_one(f"div[class*='server'][data-name='{server_id}']")

            for data in server_soup.select('li.episode > a'):
                ep_number = data.get('data-episode-num')
                ep_id = data.get('data-episode-id')
                data_id = data.get('data-id')
                ep_href = SES.build_url(data.get('href'))

                # Salto gli episodi che non sono nella lista di filtraggio (se presente)
                if nums and ep_number not in nums: continue

                if ep_id not in raw_eps:
                    raw_eps[ep_id] = {
                        'number': ep_number,
                        'id': ep_id,
                        'data': []
                    }
                
                raw_eps[ep_id]['data'].append({
                    'id': data_id,
                    'link': ep_href,
                    'serverId': server_id,
                    'serverName': server_name
                })

        return [
            Episodio(x['number'], x['id'], x['data']) 
            for x in list(raw_eps.values())
        ]