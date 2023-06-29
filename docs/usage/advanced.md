# Advanced Usage


## Eccezioni

La libreria solleva diverse eccezioni, le principali sono: [`AnimeNotAvailable`](../../api-reference/exceptions/#animeworld.exceptions.AnimeNotAvailable), [`Error404`](../../api-reference/exceptions/#animeworld.exceptions.Error404) e [`DeprecatedLibrary`](../../api-reference/exceptions/#animeworld.exceptions.DeprecatedLibrary).<br>Per maggiori informazioni consultare la [documentazione](../../api-reference/exceptions).

### DeprecatedLibrary

L'eccezione [`DeprecatedLibrary`](../../api-reference/exceptions/#animeworld.exceptions.DeprecatedLibrary) viene sollevata quando viene rivelato un mutamento del sito di [AnimeWorld](https://www.animeworld.so/) non piú supportato dalla libreria.

Questa eccezione può essere sollevata praticamente da qualsiasi metodo della libreria, quindi è consigliato gestirla in modo globale.

```py linenums="1" hl_lines="9"
try:
    res = aw.find("...")
    anime = aw.Anime("https://www.animeworld.so/play/...")
    episodi = anime.getEpisodes()

    for x in episodi:
        x.download()
        
except aw.DeprecatedLibrary as e:
    # Gestione dell'eccezione
    print("Aprire un issue su GitHub :(")
```

### Error404

L'eccezione [`Error404`](../../api-reference/exceptions/#animeworld.exceptions.Error404) viene sollevata l'URL passato alla creazione dell'oggetto Anime punta ad una pagina [404](https://www.animeworld.so/404).

Visto che questa eccezione viene sollevata solo dalla classe [`Anime`](../../api-reference/developer-interface/#animeworld.Anime), è consigliato gestirla solo se effettivamente si sta istanziando un oggetto di quella classe.

```py linenums="1" hl_lines="7"
try:
    res = aw.find("...")

    try:
        anime = aw.Anime("https://www.animeworld.so/play/...")

    except aw.Error404 as e:
        # Gestione dell'eccezione
        print("Anime non trovato :(")

    else:
        episodi = anime.getEpisodes()
        for x in episodi:
            x.download()
        
except aw.DeprecatedLibrary as e:
    # Gestione dell'eccezione
    print("Aprire un issue su GitHub :(")
```

### AnimeNotAvailable

L'eccezione [`AnimeNotAvailable`](../../api-reference/exceptions/#animeworld.exceptions.AnimeNotAvailable) viene sollevata quando la pagina dell'anime esiste ma gli episodi non sono ancora disponibili. Questo accade ad esempio quando inizia una nuova stagione e molti anime stagionali non sono ancora stati tradotti.

L'eccezione si verifica soltanto alla chiamata del metodo [`getEpisodes`](../../api-reference/developer-interface/#animeworld.anime.Anime.getEpisodes).

```py linenums="1" hl_lines="15"
try:
    res = aw.find("...")

    try:
        anime = aw.Anime("https://www.animeworld.so/play/...")

    except aw.Error404 as e:
        # Gestione dell'eccezione
        print("Anime non trovato :(")

    else:
        try:
            episodi = anime.getEpisodes()

        except aw.AnimeNotAvailable as e:
            # Gestione dell'eccezione
            print("Anime non ancora disponibile :(")

        else:
            for x in episodi:
                x.download()
        
except aw.DeprecatedLibrary as e:
    # Gestione dell'eccezione
    print("Aprire un issue su GitHub :(")
```

## Server
   
Per scarica un episodio è possibile selezione manualmente il server da cui scaricare il video. Per farlo è ottenere prima la lista dei server utilizzando l'attributo [`Episodio.links`](../../api-reference/developer-interface/#animeworld.episodio.Episodio.links) e poi sceglierne uno tra quelli supportati.

!!! Warning
    Non consiglio di utilizzare questo metodo per scaricare un episodio, è molto piú semplice e sicuro utilizzare il metodo [`Episodio.download`](../../api-reference/developer-interface/#animeworld.episodio.Episodio.download), perchè:

    1. Viene scelto sempre il server più veloce al momento del download.
    2. Se si usa un serer non supportato dalla libreria, verrà sollevata l'eccezione [ServerNotSupported](../../api-reference/exceptions/#animeworld.exceptions.ServerNotSupported).

```py linenums="1"
anime = aw.Anime("...")

# Scelgo il primo episodio
episodio = anime.getEpisodes()[0]

# Ottengo la lista dei server
servers = episodio.links

# Scelgo il server AnimeWorld_Server ad esempio
server = [x for x in servers if isinstance(x.name, AnimeWorld_Server)][0]

# Scarico il video
server.download()
```

### Server supportati

I server supportati sono querelli indicati di sotto, se vuoi contribuire ad aggiungerne altri puoi dare un occhiata alla sezione [Contributing](../../community/contributing/).

--8<-- "static/server.txt"

## Download

!!! Warning inline end
    Se ci sono dei caratteri non ammessi nel nome del file (`#%&{}<>*?/$!'":@+\``|=`), questi verranno rimossi automaticamente. Per ottenere il nome del file effettivamente scritto su disco è possibile ottenerlo dal ritorno del metodo [`Episodio.download`](../../api-reference/developer-interface/#animeworld.episodio.Episodio.download).


Per scaricare un episodio è possibile utilizzare il metodo [`Episodio.download`](../../api-reference/developer-interface/#animeworld.episodio.Episodio.download), che scarica il video utilizzando il server piú veloce al momento del download.

È possibile impostare il nome del file utilizzando il parametro `title` e la cartella di destinazione utilizzando il parametro `folder`.

### hook

Il parametro `hook` è più interessante, questo è un riferimento ad una funzione che poi verrà chiamata ogni volta che viene scaricato un chunk del video (~524 Kb). Questo è utile per mostrare a schermo il progresso del download. La funzione deve avere un singolo parametro di tipo `Dict[str, Any]`.

Un esempio di un possibile dizionario passato alla funzione hook è il seguente:

```py
{
    "total_bytes": 234127340, # Dimensione totale del video in byte
    "downloaded_bytes": 524288, # Dimensione scaricata in byte
    "percentage": 0.0022393283928310126, # Percentuale scaricata [0, 1]
    "speed": 3048288.673006227, # Velocità di download in byte/s
    "elapsed": 0.17199420928955078, # Tempo trascorso in secondi
    "filename": "1 - AnimeWorld Server.mp4", # Nome del file
    "eta": 76.63416331551707, # Tempo rimanente stimato in secondi
    "status": "downloading", # Stato del download ('downloading' | 'finished' | 'aborted')
}
```

### opt

È anche possibile fermare forzatamente il download utilizzando il parametro `opt`. Questo parametro è una lista di stringhe, ogni stringa rappresenta un'opzione. Attualmente l'unica opzione possibile è `abort`, che ferma il download. 

Se in opt compare, durante il download, la stringa `abort` allora il download viene fermato e il file parzialmente scaricato viene eliminato.

Un esempio di utilizzo del parametro `opt` è il seguente:

```py linenums="1"
import animeworld as aw
import time
from threading import Thread

anime = aw.Anime("...")
episodio = anime.getEpisodes()[0]

# Definisco la funzione per il thread
def gestioneDownload(lista_opzioni):
    time.sleep(5)
    lista_opzioni.append("abort")


opt = [] # Array per le opzioni dinamiche
t = Thread(target=gestioneDownload, args=(opt,)) # Creo il thread

t.start() # Avvio il thread

episodio.download(opt=opt) # Avvio il download
```

In questo esempio il download viene fermato dopo 5 secondi.

---

## Esempio completo

```py title="example.py" linenums="1"
--8<-- "static/example.py"
```
