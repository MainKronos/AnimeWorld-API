import os, time
from typing import Dict, List, Optional, Callable
from datetime import datetime
import youtube_dl

from ..utility import SES
from ..exceptions import ServerNotSupported, HardStoppedDownload

class Server:
    """
    Attributes:
      link: Link del server in cui è hostato l'episodio.
      Nid: ID del server.
      name: Nome del server.
      number: Numero dell'episodio.
    """

    def __init__(self, link: str, Nid: int, name: str, number: str):
        """
        Args:
          link: Link del server in cui è hostato l'episodio.
          Nid: ID del server.
          name: Nome del server.
          number: Numero dell'episodio.
        """

        self.link:str = link
        self.Nid:int = Nid
        self.name:str = name
        self.number:str = number

        # self._HDR = HDR # Protected 
        self._defTitle = f"{self.number} - {self.name}" # nome del file provvisorio

    def _sanitize(self, title: str) -> str: # Toglie i caratteri illegali per i file
        """
        Rimuove i caratteri illegali per il nome del file.

        Args:
          title: Nome del file.
        
        Returns:
          Il nome del file sanitizzato.
          
        Example:
          ```py
          return str # title sanitizzato
          ```
        """
        illegal = ['#','%','&','{','}', '\\','<','>','*','?','/','$','!',"'",'"',':','@','+','`','|','=']
        for x in illegal:
            title = title.replace(x, '')
        return title

    def fileInfo(self) -> dict[str,str]:
        """
        Recupera le informazioni del file dell'episodio.

        Returns:
          Informazioni file episodio.
        
        Raises:
          ServerNotSupported: Se il server non è supportato.

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

        raise ServerNotSupported(self.name)
    
    def fileLink(self) -> str:
        """
        Recupera il link diretto per il download del file dell'episodio.

        Returns:
            Link diretto.
        
        Raises:
          ServerNotSupported: Se il server non è supportato.
        
        Example:
          ```py
          return str # Link del file
          ```
        """

        raise ServerNotSupported(self.name)
    
    def _fileInfoIn(self) -> Dict[str,str]:
        """
        Recupera le informazioni del file dell'episodio usando httpx.
        """
        url = self.fileLink()

        r = SES.head(url)
        r.raise_for_status()

        return {
            "content_type": r.headers['content-type'],
            "total_bytes": int(r.headers['Content-Length']),
            "last_modified": datetime.strptime(r.headers['Last-Modified'], "%a, %d %b %Y %H:%M:%S %Z"),
            "server_name": self.name,
            "server_id": self.Nid,
            "url": url
        }
    
    def _fileInfoEx(self) -> Dict[str,str]:
        """
        Recupera le informazioni del file dell'episodio usando yutube_dl.
        """

        class MyLogger(object):
            def debug(self, msg):
                pass
            def warning(self, msg):
                pass
            def error(self, msg):
                print(msg)
                return False
        
        ydl_opts = {
            'logger': MyLogger()
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = self.fileLink()
            info = ydl.extract_info(url, download=False)
            return {
                "content_type": "unknown",
                "total_bytes": -1,
                "last_modified": datetime.fromtimestamp(0),
                "server_name": self.name,
                "server_id": self.Nid,
                "url": url
            }


    def download(self, title: Optional[str]=None, folder: str='', *, hook: Callable[[Dict], None]=lambda *args:None, opt: List[str]=[]) -> Optional[str]:
        """
        Scarica l'episodio dal primo server funzionante della lista links.

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
          ServerNotSupported: Se il server non è supportato.
          HardStoppedDownload: Il file in download è stato forzatamente interrotto.

        Example:
          ```py
          return str # File scaricato
          ```
        """
        raise ServerNotSupported(self.name)

    # Protected
    def _downloadIn(self, title: str, folder: str, *, hook: Callable[[Dict], None], opt: List[str]) -> Optional[str]: # Scarica l'episodio

        """
        Scarica il file utilizzando httpx.

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
        with SES.stream("GET", self.fileLink(), follow_redirects=True) as r:
            r.raise_for_status()
            ext = r.headers['content-type'].split('/')[-1]
            if ext == 'octet-stream': ext = 'mp4'
            file = f"{title}.{ext}"

            total_length = int(r.headers.get('content-length'))
            current_lenght = 0
            start = time.time()
            step = time.time()

            try:
                with open(f"{os.path.join(folder,file)}", 'wb') as f:
                    for chunk in r.iter_bytes(chunk_size = 524288):
                        if chunk: 
                            f.write(chunk)
                            f.flush()
                            
                            current_lenght += len(chunk)

                            hook({
                                'total_bytes': total_length,
                                'downloaded_bytes': current_lenght,
                                'percentage': current_lenght/total_length,
                                'speed': len(chunk) / (time.time() - step) if (time.time() - step) != 0 else 0,
                                'elapsed': time.time() - start,
                                'filename': file,
                                'eta': ((total_length - current_lenght) / len(chunk)) * (time.time() - step),
                                'status': 'downloading' if "abort" not in opt else "aborted"
                            })

                            if "abort" in opt: raise HardStoppedDownload(file)

                            step = time.time()
                            
                    else:
                        hook({
                            'total_bytes': total_length,
                            'downloaded_bytes': total_length,
                            'percentage': 1,
                            'speed': 0,
                            'elapsed': time.time() - start,
                            'eta': 0,
                            'status': 'finished'
                        })

                        return file # Se il file è stato scaricato correttamente
            except HardStoppedDownload:
                os.remove(f"{os.path.join(folder,file)}")
                return None

    # Protected
    def _dowloadEx(self, title: str, folder: str, *, hook: Callable[[Dict], None], opt: List[str]) -> Optional[str]:
        """
        Scarica il file utilizzando yutube_dl.

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

        class MyLogger(object):
            def debug(self, msg):
                pass
            def warning(self, msg):
                pass
            def error(self, msg):
                print(msg)
                return False

        def my_hook(d):

            hook({
                'total_bytes': int(d['total_bytes_estimate']),
                'downloaded_bytes': int(d['downloaded_bytes']),
                'percentage': int(d['downloaded_bytes'])/int(d['total_bytes_estimate']),
                'speed': float(d['speed']) if d['speed'] is not None else 0,
                'elapsed': float(d['elapsed']),
                'filename': d['filename'],
                'eta': int(d['eta']),
                'status': d['status'] if "abort" not in opt else "aborted"
            })

            if "abort" in opt: raise HardStoppedDownload(d['filename'])

        ydl_opts = {
            'outtmpl': f"{os.path.join(folder,title)}.%(ext)s",
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = self.fileLink()
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            try:
                ydl.download([url])
            except HardStoppedDownload:
                os.remove(f"{os.path.join(folder,filename)}")
                return None
            return filename