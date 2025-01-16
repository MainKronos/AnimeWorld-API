# QuickStart

Per prima cosa importiamo la libreria:

```python linenums="1"
import animeworld as aw
```

## Find

Adesso proviamo a cercare un anime:

```python linenums="2"
res = aw.find("Sword Art Online")
print(res)
```
??? Example "Output"

    ```python
    [
        {
            "id": 1717,
            "name": "Sword Art Online",
            "jtitle": "Sword Art Online",
            "studio": "A-1 Pictures",
            "release": "05 Luglio 2014",
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

```py linenums="4"
anime = aw.Anime("https://www.animeworld.so/play/sword-art-online.N0onT")
```

!!! warning 
    Se il link passato punta ad una pagina [404](https://www.animeworld.so/404) verrannà sollevata l'eccezione [Error404](../../api-reference/exceptions/#animeworld.exceptions.Error404).

Con questa classe è possibile ottenere informazioni sull'anime: 

```py linenums="5"
# Il titolo
print("Titolo:", anime.getName())
print("----------------------------------\n")

# La trama
print("Trama:", anime.getTrama())
print("----------------------------------\n")

# La locandina
print("Cover: ", anime.getCover())
print("----------------------------------\n")

# Informazioni generali
info = anime.getInfo()
print("Informazioni generali:\n", "\n".join(
    [f"{x}: {info[x]}" for x in info]
))
print("----------------------------------\n")
```

??? Example "Output"

    ```
    Titolo: Sword Art Online
    ----------------------------------

    Trama: Kazuto "Kirito" Kirigaya, un genio della programmazione, entra in una realtà  virtuale interattiva con pluralità  di giocatori (una realtà  "massively multi-player online" o "MMO") denominata "Sword Art Online". Il problema sta nel fatto che, una volta entrati, se ne può uscire solo vincitori, completando il gioco, perché il game over equivale a morte certa del giocatore.
    ----------------------------------

    Informazioni generali:
    Categoria: Anime
    Audio: Giapponese
    Data di Uscita: 08 Luglio 2012
    Stagione: Estate 2012
    Studio: A-1 Pictures
    Genere: ['Avventura', 'Azione', 'Fantasy', 'Gioco', 'Romantico', 'Sentimentale']
    Voto: 8.36 / 10
    Durata: 23 min/ep
    Episodi: 25
    Stato: Finito
    Visualizzazioni: 461.733
    ----------------------------------
    ```

Ma soprattutto scaricare gli episodi:

!!! Quote inline end "" 

    !!! Info 
        Se al metodo `getEpisodes()` non viene passato nessun argomento, verranno ottenuti **TUTTI** gli episodi dell'anime.

    !!! Warning
        `ep.number` è un attributo di tipo `str`, maggiori informazioni [qui](../../api-reference/developer-interface/#animeworld.Episodio).



```py linenums="19"
# Ottengo una lista di Episodi
# che mi interessano
episodi = anime.getEpisodes([1, 2, 4])


# E li scarico
for ep in episodi:

    print(f"Scarico l'episodio {ep.number}.")

    # Uno alla volta...
    ep.download() 

    print(f"Download completato.")
```

??? Example "Output"

    ```
    Scarico l'episodio 1.
    Download completato.
    Scarico l'episodio 2.
    Download completato.
    Scarico l'episodio 4.
    Download completato.
    ```