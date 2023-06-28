# QuickStart

Per prima cosa importiamo la libreria:

```python
>>> import animeworld as aw
```

## Find

Adesso proviamo a cercare un anime:

???+ example

    ```python
    >>> aw.find("Sword Art Online")
    >>> res
    [
        {
            "id": 1717,
            "name": "Sword Art Online",
            "jtitle": "Sword Art Online",
            "studio": "A-1 Pictures",
            "release": datetime.datetime(2012, 7, 8, 0, 0),
            "episodes": 25,
            "state": "1",
            "story": 'Kazuto "Kirito" Kirigaya, un genio della programmazione, entra in una realtà  virtuale interattiva con pluralità  di giocatori (una realtà  "massively multi-player online" o "MMO") denominata "Sword Art Online". Il problema sta nel fatto che, una volta entrati, se ne può uscire solo vincitori, completando il gioco, perché il game over equivale a morte certa del giocatore.',
            "categories": [...],
            "image": "https://img.animeworld.so/locandine/36343l.jpg",
            "durationEpisodes": "23",
            "link": "https://www.animeworld.so/play/sword-art-online.N0onT",
            "createdAt": "2020-08-02T15:42:44.000Z",
            "language": "jp",
            "year": "2012",
            "dub": False,
            "season": "summer",
            "totViews": 461576,
            "dayViews": 204,
            "weekViews": 459,
            "monthViews": 6416,
            "malId": 11757,
            "anilistId": 11757,
            "mangaworldId": None,
            "malVote": 7.35,
            "trailer": "https://www.youtube.com/embed/6ohYYtxfDCg?enablejsapi=1&wmode=opaque",
        },
        ...
    ]
    ```

La funzione [find](../../api-reference/developer-interface/#animeworld.find) restituisce una lista di dizionari, uno per ogni anime trovato. Ogni dizionario contiene molte informazioni, tra cui: il nome, il numero di episodi, la data di uscita, il link, ecc. 

## Anime



La classe [Anime](../../api-reference/developer-interface/#animeworld.Anime) è l'oggetto che stà alla base di questa libreria. Per istanziarla è necessario passare il link dell'anime, ottenuto direttamente dal sito di [AnimeWorld](https://www.animeworld.so/) o dalla funzione [find](../../api-reference/developer-interface/#animeworld.find) vista prima.

```py 
>>> anime = aw.Anime("https://www.animeworld.so/play/sword-art-online.N0onT")
```

!!! warning 
    Se il link passato punta ad una pagina [404](https://www.animeworld.so/404) o ad un anime non ancora disponibile, verranno sollevate le rispettive eccezioni [Error404](../../api-reference/exceptions/#animeworld.exceptions.Error404) e [AnimeNotAvailable](../../api-reference/exceptions/#animeworld.exceptions.AnimeNotAvailable).

Con questa classe è possibile ottenere molte informazioni sull'anime: 

```py
>>> anime.getInfo()
```

//TODO: da continuare