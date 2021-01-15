![AnimeWorld](/documentation/img/AWGIFLOGO2.gif)
# AnimeWorld-API
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
```
{
    'No Game no Life': 'https://www.animeworld.tv/play/no-game-no-life.IJUH1',
    'No Game No Life: Zero': 'https://www.animeworld.tv/play/no-game-no-life-zero.p-2vq'
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
Per un utilizzo avanzato consultare la [documentazione](../../wiki).
