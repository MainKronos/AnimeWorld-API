# QuickStart

First, let's import the library:

```python linenums="1"
import animeworld as aw
```

## Find

Now let's try searching for an anime:

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

The [find](../../api-reference/developer-interface/#animeworld.find) function returns a list of dictionaries, one for each found anime. Each dictionary contains many details, including the name, episode count, release date, link, etc.

## Anime

The [Anime](../../api-reference/developer-interface/#animeworld.Anime) class is the core object of this library. To instantiate it, you need to pass the anime link, obtained directly from the [AnimeWorld](https://www.animeworld.so/) site or from the [find](../../api-reference/developer-interface/#animeworld.find) function seen earlier.

```python linenums="4"
anime = aw.Anime("https://www.animeworld.so/play/sword-art-online.N0onT")
```

!!! warning 
    If the passed link points to a [404](https://www.animeworld.so/404) page, the [Error404](../../api-reference/exceptions/#animeworld.exceptions.Error404) exception will be raised.

With this class, you can obtain information about the anime:

```python linenums="5"
# Title
print("Title:", anime.getName())
print("----------------------------------\n")

# Plot
print("Plot:", anime.getTrama())
print("----------------------------------\n")

# Cover
print("Cover: ", anime.getCover())
print("----------------------------------\n")

# General information
info = anime.getInfo()
print("General Information:\n", "\n".join(
    [f"{x}: {info[x]}" for x in info]
))
print("----------------------------------\n")
```

??? Example "Output"

    ```
    Title: Sword Art Online
    ----------------------------------

    Plot: Kazuto "Kirito" Kirigaya, un genio della programmazione, entra in una realtà  virtuale interattiva con pluralità  di giocatori (una realtà  "massively multi-player online" o "MMO") denominata "Sword Art Online". Il problema sta nel fatto che, una volta entrati, se ne può uscire solo vincitori, completando il gioco, perché il game over equivale a morte certa del giocatore.
    ----------------------------------

    General Information:
    Category: Anime
    Audio: Giapponese
    Release Date: 08 Luglio 2012
    Season: Estate 2012
    Studio: A-1 Pictures
    Genre: ['Avventura', 'Azione', 'Fantasy', 'Gioco', 'Romantico', 'Sentimentale']
    Rating: 8.36 / 10
    Duration: 23 min/ep
    Episodes: 25
    Status: Finito
    Views: 461.733
    ----------------------------------
    ```

But most importantly, download the episodes:

!!! Quote inline end "" 

    !!! Info 
        If no argument is passed to the `getEpisodes()` method, **ALL** episodes of the anime will be obtained.

    !!! Warning
        `ep.number` is an attribute of type `str`, more information [here](../../api-reference/developer-interface/#animeworld.Episodio).



```python linenums="19"
# Obtain a list of episodes
# that interest me
episodes = anime.getEpisodes([1, 2, 4])


# And download them
for ep in episodes:

    print(f"Downloading episode {ep.number}.")

    # One at a time...
    ep.download() 

    print(f"Download completed.")
```

??? Example "Output"

    ```
    Downloading episode 1.
    Download completed.
    Downloading episode 2.
    Download completed.
    Downloading episode 4.
    Download completed.
    ```