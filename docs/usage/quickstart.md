# QuickStart

Per priuma cosa importiamo la libreria:

```python
>>> import animeworld as aw
```

### Find

Adesso proviamo a cercare un anime:

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