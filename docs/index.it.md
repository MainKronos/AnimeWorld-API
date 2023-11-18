<p align="center" style="margin: 0 0 10px">
  <img height="208" src="../static/img/AnimeWorld-API.png" alt='AnimeWorld-API'>
</p>

---

# Welcome to AnimeWorld-API wiki!

AnimeWorld-API is an UNOFFICIAL library for AnimeWorld (Italian anime site).

---

Installa la libreria tramite pip: 
```bash
$ pip install animeworld
```

Adesso puoi iniziare a cercare anime:
```python
>>> import animeworld as aw
>>> res = aw.find("No game no life")
>>> res
{'name': 'No Game no Life', 'link': 'https://www.animeworld.so/play/no-game-no-life.IJUH1', ...}
```

E a scaricare episodi:
```python
>>> import animeworld as aw
>>> anime = aw.Anime(link="https://www.animeworld.so/play/danmachi-3.Ydt8-")
>>> for episodio in anime.getEpisodes():
...     print("Episodio Numero: ", episodio.number)
...     if(episodio.download()):
...         print("Download completato")
```

## Documentazione

Per una panoramica di tutte le nozioni di base, vai alla sezione [QuickStart](usage/quickstart.md)

Per argomenti più avanzati, vedere la sezione [Advanced Usage](usage/advanced.md)

La sezione [API Reference](api-reference/developer-interface.md) fornisce un riferimento API completo.

Se vuoi contribuire al progetto, vai alla sezione [Contributing](community/contributing.md)

## Dipendenze

- [`httpx`](https://github.com/encode/httpx) - A next generation HTTP client for Python.

- [`youtube_dl`](https://github.com/ytdl-org/youtube-dl) - Command-line program to download videos from YouTube.com and other video sites.

- [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping.