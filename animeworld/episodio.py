"""
Modulo contenente la struttura a classe degli episodi.
"""
import httpx
from bs4 import BeautifulSoup
from typing import *
import time
import io

from .utility import SES
from .exceptions import ServerNotSupported
from .servers import AnimeWorld_Server
from .servers.Server import Server

class Episodio:
    """
    Attributes:
      number: Numero dell'episodio.
      links: Lista dei server in cui è hostato l'episodio.

    Warning:
      L'attributo `number` è di tipo `str` perchè è possibile che capitino episodi con un numero composto (es. `5.5`, `268-269`), è un caso molto raro ma possibile.
    """

    def __init__(self, ep_number: str, ep_id: str, data: List[Dict] = []):
        """
        Args:
          ep_number: Numero dell'episodio.
          ep_id: Numerazione globale dell'episodio.
          data: Lista delle informazioni per scaricare l'episodio per ogni server trovato.
        """
        self.number:str = ep_number
        self.__id:str = ep_id
        self.__data:List[Dict] = data

    @property
    def links(self) -> Iterator[Server]: # lista dei provider dove sono hostati gli ep
        """
        Ottiene la lista dei server in cui è hostato l'episodio.

        Returns:
          Lista di oggetti Server.
        
        Example:
          ```py
          return [
            Server, # Classe Server
            ...
          ]
          ```
        """

        for info in self.__data:
            data_id = info.get('id')
            server_id = info.get('serverId')
            server_name = info.get('serverName')

            res = SES.get('/api/episode/info', params={'id': data_id, 'alt': 0})
            res.raise_for_status()
            data = res.json()

            if 'grabber' not in data: continue

            match server_id:
                # AnimeWorld Server
                case 9:
                    yield AnimeWorld_Server(data['grabber'], server_id, server_name, self.number)
                # Server generico
                case _:
                    yield Server(data['grabber'], server_id, server_name, self.number)


    def fileInfo(self) -> Dict[str,str]:
        """
        Recupera le informazioni del file dell'episodio.

        Returns:
          Informazioni file episodio.

        Example:
          ```py
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

    def download(self, title: Optional[str]=None, folder: Union[str, io.IOBase]='', *, hook: Callable[[Dict], None]=lambda *args:None, opt: List[str]=[]) -> Optional[str]: # Scarica l'episodio con il primo link nella lista
        """
        Scarica l'episodio dal server più veloce.

        Args:
          title: Nome con cui verrà nominato il file scaricato.
          folder: Posizione in cui verrà spostato il file scaricato.

        Other parameters:
          hook: Funzione che viene richiamata varie volte durante il download; la funzione riceve come argomento un dizionario con le seguenti chiavi:\n 
            - `total_bytes`: Byte totali da scaricare.
            - `downloaded_bytes`: Byte attualmente scaricati.
            - `percentage`: Percentuale del progresso di download.
            - `speed`: Velocità di download (byte/s)
            - `elapsed`: Tempo trascorso dall'inizio del download.
            - `eta`: Tempo stimato rimanente per fine del download.
            - `status`: 'downloading' | 'finished' | 'aborted'
            - `filename`: Nome del file in download.

          opt: Lista per delle opzioni aggiuntive.\n
            - `'abort'`: Ferma forzatamente il download.
        
        Returns:
          Nome del file scaricato. 
        
        Raises:
          HardStoppedDownload: Il file in download è stato forzatamente interrotto.

        Example:
          ```py
          return str # File scaricato
          ```
        """

        return self.__choiceBestServer().download(title,folder,hook=hook,opt=opt)
    
    def __choiceBestServer(self) -> Server:
        """
        Sceglie il server più veloce per il download dell'episodio.

        Returns:
          Il Server più veloce.
        """
        return next(self.links) # ritorno il primo server, che è quello più veloce (viene ordinato in __sortServer)