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

--8<-- "static/server.md"

---

## Esempio completo

```py title="example.py" linenums="1"
--8<-- "static/example.py"
```

//TODO: da ampliare