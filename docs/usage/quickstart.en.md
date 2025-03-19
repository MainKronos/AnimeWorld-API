# QuickStart

First, let's import the library:

```python linenums="1"
import animeworld as aw
```

## Session (Optional)

It may be necessary to change the `base_url` of all links if the AnimeWorld site changes from `https://www.animeworld.ac` to something else.

To do this, you need to modify the session's `base_url` [(SES)][animeworld.SES]:

```python linenums="2"
aw.SES.base_url = "https://www.animeworld.ac"
```

## Find

Now let's try searching for an anime:

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
            "release": "July 5, 2014",
            "episodes": 25,
            "state": "1",
            "story": 'Kazuto "Kirito" Kirigaya, a programming genius, enters an interactive virtual reality with multiple players (a "massively multiplayer online" or "MMO") called "Sword Art Online." The problem is that once inside, players can only leave by winning the game—because "game over" means certain death.',
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

The [find][animeworld.find] function returns a list of dictionaries, one for each anime found. Each dictionary contains a lot of information, including the name, number of episodes, release date, link, etc.

## Anime

The [Anime][animeworld.Anime] class is the core object of this library. To instantiate it, you need to pass the anime's link, which can be obtained directly from the [AnimeWorld](https://www.animeworld.ac/) website or from the previously mentioned [find][animeworld.find] function.

```py linenums="5"
# https://www.animeworld.ac/play/sword-art-online.N0onT
anime = aw.Anime("/play/sword-art-online.N0onT")
```

!!! warning 
    You can pass the full link to the `Anime` class, like this:
    ```py
    anime = aw.Anime("https://www.animeworld.ac/play/sword-art-online.N0onT")
    ```
    However, the `base_url` (`https://www.animeworld.ac`) will be replaced with the one defined in the Session [(SES)][animeworld.SES].

!!! warning 
    If the provided link points to a [404](https://www.animeworld.ac/404) page, the exception [Error404][animeworld.exceptions.Error404] will be raised.

With this class, you can retrieve information about the anime:

```py linenums="7"
# Title
print("Title:", anime.getName())
print("----------------------------------\n")

# Synopsis
print("Synopsis:", anime.getTrama())
print("----------------------------------\n")

# Cover image
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

    Synopsis: Kazuto "Kirito" Kirigaya, a programming genius, enters an interactive virtual reality with multiple players (a "massively multiplayer online" or "MMO") called "Sword Art Online." The problem is that once inside, players can only leave by winning the game—because "game over" means certain death.
    ----------------------------------

    General Information:
    Category: Anime
    Audio: Japanese
    Release Date: July 8, 2012
    Season: Summer 2012
    Studio: A-1 Pictures
    Genre: ['Adventure', 'Action', 'Fantasy', 'Game', 'Romance', 'Drama']
    Score: 8.36 / 10
    Duration: 23 min/ep
    Episodes: 25
    Status: Completed
    Views: 461,733
    ----------------------------------
    ```

Most importantly, you can download the episodes:

!!! Quote inline end "" 

    !!! Info 
        If no argument is passed to the `getEpisodes()` method, **ALL** episodes of the anime will be retrieved.

    !!! Warning
        `ep.number` is a `str` attribute. More information [here][animeworld.Episodio].



```py linenums="20"
# Get a list of episodes
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