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

## Installazione
Questa libreria richiede [Python 3.11](https://www.python.org/) o superiore.

È Possibile installarare la libreria tramite pip:
```shell script
pip install animeworld
```

## Utilizzo
Per ricercare un anime per nome nel sito di animeWolrd è possibile usare la funzione find().
```python
import animeworld as aw

res = aw.find("No game no life")
print(res)
```
La funzione estituirà un dizionario contentente per chiave il nome dell'anime e per valore il link della pagina di animeworld.
```python
{'name': 'No Game no Life', 'link': 'https://www.animeworld.ac/play/no-game-no-life.IJUH1E', ...}
```
È Possibile anche scaricare gli episodi di un anime.
```python
import animeworld as aw

anime = aw.Anime(link="https://www.animeworld.ac/play/danmachi-3.Ydt8-")
for episodio in anime.getEpisodes():
    print("Episodio Numero: ", episodio.number)
        
    if(episodio.download()):
        print("scaricato")
    else:
        print("errore")

    if episodio.number == '1': break
```
```
Episodio Numero: 1
scaricato
```

## Documentazione

La documentazione completa è disponibile qui: [Documentazione](https://mainkronos.github.io/AnimeWorld-API/)

Per una panoramica di tutte le nozioni di base, vai alla sezione [QuickStart](https://mainkronos.github.io/AnimeWorld-API/usage/quickstart)

Per argomenti più avanzati, vedere la sezione [Advanced Usage](https://mainkronos.github.io/AnimeWorld-API/usage/advanced)

La sezione [API Reference](https://mainkronos.github.io/AnimeWorld-API/api-reference/developer-interface) fornisce un riferimento API completo.

Se vuoi contribuire al progetto, vai alla sezione [Contributing](https://mainkronos.github.io/AnimeWorld-API/community/contributing)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MainKronos/AnimeWorld-API&type=Date)](https://star-history.com/#MainKronos/AnimeWorld-API&Date)
