![AnimeWorld](/documentation/img/AnimeWorld-API.png)
# AnimeWorld-API

![Version](https://img.shields.io/pypi/v/animeworld)
![Activity](https://img.shields.io/github/commit-activity/w/MainKronos/AnimeWorld-API) 
![Publish to PyPI](https://github.com/MainKronos/AnimeWorld-API/workflows/Publish%20to%20PyPI/badge.svg)

![PyPI - Downloads](https://img.shields.io/pypi/dm/animeworld)
![PyPI - Downloads](https://img.shields.io/pypi/dw/animeworld)
![PyPI - Downloads](https://img.shields.io/pypi/dd/animeworld)

AnimeWorld-API is an unofficial library for [AnimeWorld](https://www.animeworld.tv/) (Italian anime site).

## Installazione
Questa libreria richiede [Python 3.6](https://www.python.org/) o superiore.

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
{
	'name': 'No Game no Life',
	'link': 'https://www.animeworld.tv/play/no-game-no-life.IJUH1'
}
```
È Possibile anche scaricare gli episodi di un anime.
```python
import animeworld as aw

anime = aw.Anime(link="https://www.animeworld.tv/play/danmachi-3.Ydt8-")
for episodio in anime.getEpisodes():
    print("Episodio Numero: ", episodio.number)
        
    if(episodio.download()):
        print("scaricato")
    else:
        print("errore")

    if x.number == '1': break
```
```
Episodio Numero: 1
scaricato
```

## Utilizzo Avanzato
Per testare velocemete le funzionalità della libreria è possibile usare e consultare il file di esempio: [`example.py`](/documentation/example.py).

Per un utilizzo avanzato consultare la [documentazione](https://github.com/MainKronos/AnimeWorld-API/wiki).

## Contributing
Se volete contribuire aprendo Issue o Pull a questa libreria siete ben accetti, tutto il codice sorgente e la documentazione è reperible su [GitHub](https://github.com/MainKronos/AnimeWorld-API).
