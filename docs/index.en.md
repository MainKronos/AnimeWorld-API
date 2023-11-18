<p align="center" style="margin: 0 0 10px">
  <img height="208" src="static/img/AnimeWorld-API.png" alt='AnimeWorld-API'>
</p>

---

# Welcome to AnimeWorld-API wiki!

AnimeWorld-API is an UNOFFICIAL library for AnimeWorld (Italian anime site).

---

## Installation
Install the library using pip:
```bash
$ pip install animeworld
```

Now you can start searching for anime:
```python
>>> import animeworld as aw
>>> res = aw.find("No game no life")
>>> res
{'name': 'No Game no Life', 'link': 'https://www.animeworld.so/play/no-game-no-life.IJUH1', ...}
```

And download episodes:
```python
>>> import animeworld as aw
>>> anime = aw.Anime(link="https://www.animeworld.so/play/danmachi-3.Ydt8-")
>>> for episode in anime.getEpisodes():
...     print("Episode Number: ", episode.number)
...     if(episode.download()):
...         print("Download completed")
```

## Documentation

For an overview of all the basics, go to the [QuickStart](usage/quickstart.md) section.

For more advanced topics, see the [Advanced Usage](usage/advanced.md) section.

The [API Reference](api-reference/developer-interface.md) section provides a complete API reference.

If you want to contribute to the project, visit the [Contributing](community/contributing.md) section.

## Dependencies

- [`httpx`](https://github.com/encode/httpx) - A next-generation HTTP client for Python.

- [`youtube_dl`](https://github.com/ytdl-org/youtube-dl) - Command-line program to download videos from YouTube.com and other video sites.

- [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping.