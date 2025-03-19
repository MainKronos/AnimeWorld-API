[![AnimeWorld](https://github.com/MainKronos/AnimeWorld-API/blob/master/docs/static/img/AnimeWorld-API.png)](https://mainkronos.github.io/AnimeWorld-API/)
# AnimeWorld-API

[![Version](https://img.shields.io/pypi/v/animeworld)](https://github.com/MainKronos/AnimeWorld-API/releases/latest)
![Activity](https://img.shields.io/github/commit-activity/w/MainKronos/AnimeWorld-API) 
[![Publish to PyPI](https://github.com/MainKronos/AnimeWorld-API/workflows/Publish%20to%20PyPI/badge.svg)](https://pypi.org/project/animeworld/)
[![Deploy MkDocs](https://github.com/MainKronos/AnimeWorld-API/actions/workflows/deploy-mkdocs.yml/badge.svg)](https://github.com/MainKronos/AnimeWorld-API/actions/workflows/deploy-mkdocs.yml)

![PyPI - Downloads](https://img.shields.io/pypi/dm/animeworld)
![PyPI - Downloads](https://img.shields.io/pypi/dw/animeworld)
![PyPI - Downloads](https://img.shields.io/pypi/dd/animeworld)

[![Static Badge](https://img.shields.io/badge/lang-english-%239FA8DA)](https://github.com/MainKronos/AnimeWorld-API/blob/master/README.md)
[![Static Badge](https://img.shields.io/badge/lang-italian-%239FA8DA)](https://github.com/MainKronos/AnimeWorld-API/blob/master/README.it.md)


AnimeWorld-API is an unofficial library for [AnimeWorld](https://www.animeworld.ac/) (Italian anime site).

## Installation
This library requires [Python 3.7](https://www.python.org/) or later.

You can install the library using pip:
```shell script
pip install animeworld
```

## Usage
To search for an anime by name on the AnimeWorld site, you can use the `find()` function.
```python
import animeworld as aw

res = aw.find("No game no life")
print(res)
```
The function will return a dictionary with the anime name as the key and the link to the anime world page as the value.
```python
{'name': 'No Game no Life', 'link': 'https://www.animeworld.ac/play/no-game-no-life.IJUH1E', ...}
```
You can also download episodes of an anime.
```python
import animeworld as aw

anime = aw.Anime(link="https://www.animeworld.ac/play/danmachi-3.Ydt8-")
for episode in anime.getEpisodes():
    print("Episode Number: ", episode.number)
        
    if(episode.download()):
        print("Downloaded")
    else:
        print("Error")

    if episode.number == '1': break
```
```
Episode Number: 1
Downloaded
```

## Documentation

The complete documentation is available here: [Documentation](https://mainkronos.github.io/AnimeWorld-API/)

For an overview of all the basics, go to the [QuickStart](https://mainkronos.github.io/AnimeWorld-API/usage/quickstart) section.

For more advanced topics, see the [Advanced Usage](https://mainkronos.github.io/AnimeWorld-API/usage/advanced) section.

The [API Reference](https://mainkronos.github.io/AnimeWorld-API/api-reference/developer-interface) section provides a complete API reference.

If you want to contribute to the project, visit the [Contributing](https://mainkronos.github.io/AnimeWorld-API/community/contributing) section.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MainKronos/AnimeWorld-API&type=Date)](https://star-history.com/#MainKronos/AnimeWorld-API&Date)
