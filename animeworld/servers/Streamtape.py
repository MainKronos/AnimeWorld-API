from bs4 import BeautifulSoup
import re

from .Server import *
from ..utility import HealthCheck

class Streamtape(Server):
    @HealthCheck
    def fileLink(self) -> str:
        """
        Recupera il link diretto per il download del file dell'episodio.

        Returns:
          Link diretto.

        Example:
          ```py
          return str # Link del file
          ```
        """
        
        sb_get = SES.get(self.link)

        if sb_get.status_code == 200:
            soupeddata = BeautifulSoup(sb_get.content, "html.parser")

            raw_link = re.search(r"document\.getElementById\('ideoooolink'\)\.innerHTML = (\".*'\))", soupeddata.prettify()).group(1)

            raw_link = raw_link.replace('"', '').replace("'", "").replace('+', '')

            raw_link_part2 = re.search(r"\((.*?)\)", raw_link).group(1)[4:]
            raw_link_part1 = re.sub(r"\(.*?\)",'', raw_link)

            mp4_link = 'http:/' + (raw_link_part1 + raw_link_part2).replace(' ', '')

            return mp4_link
    
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

        return self._fileInfoIn()

    def download(self, title: Optional[str]=None, folder: str='', *, hook: Callable[[Dict], None]=lambda *args:None, opt: List[str]=[]) -> Optional[str]:
        """
        Scarica l'episodio.

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
        if title is None: title = self._defTitle
        else: title = self._sanitize(title)
        return self._downloadIn(title,folder,hook=hook,opt=opt)