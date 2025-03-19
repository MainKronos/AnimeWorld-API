# QuickStart

Per prima cosa importiamo la libreria:

```python linenums="1"
import animeworld as aw
```

## Sessione (Opzionale)

Potrebbe essere necessario cambiare il base_url di tutti i link se il sito di animeworld cambia da `https://www.animeworld.ac` a qualcos'altro.

Per fare ciò è necessario cambiare il base_url della sessione [(SES)][animeworld.SES]

```python linenums="2"
aw.SES.base_url = "https://www.animeworld.ac"
```

## Find

Adesso proviamo a cercare un anime:

```python linenums="3"
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
            "image": "https://img.animeworld.ac/locandine/36343l.jpg",
            "durationEpisodes": "23",
            "link": "https://www.animeworld.ac/play/sword-art-online.N0onT",
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

La funzione [find][animeworld.find] restituisce una lista di dizionari, uno per ogni anime trovato. Ogni dizionario contiene molte informazioni, tra cui: il nome, il numero di episodi, la data di uscita, il link, ecc. 

## Anime

La classe [Anime][animeworld.Anime] è l'oggetto che stà alla base di questa libreria. Per istanziarla è necessario passare il link dell'anime, ottenuto direttamente dal sito di [AnimeWorld](https://www.animeworld.ac/) o dalla funzione [find][animeworld.find] vista prima.

```py linenums="5"
# https://www.animeworld.ac/play/sword-art-online.N0onT
anime = aw.Anime("/play/sword-art-online.N0onT")
```

!!! warning 
    È possibile passare il link completo alla classe Anime come ad esempio:
    ```py
    anime = aw.Anime("https://www.animeworld.ac/play/sword-art-online.N0onT")
    ```
    Ma il base_url (https://www.animeworld.ac) verrà rimpiazzato con quello definito nella Sessione [(SES)][animeworld.SES]. 

!!! warning 
    Se il link passato punta ad una pagina [404](https://www.animeworld.ac/404) verrannà sollevata l'eccezione [Error404][animeworld.exceptions.Error404].

Con questa classe è possibile ottenere informazioni sull'anime: 

```py linenums="7"
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
        `ep.number` è un attributo di tipo `str`, maggiori informazioni [qui][animeworld.Episodio].



```py linenums="20"
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