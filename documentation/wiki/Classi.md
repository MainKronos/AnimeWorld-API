# **class** Anime

| [**Attributes**](#attributes) | [**Methods**](#methods) |
| :---: | :---: |
| [`link`](#link) | [`getTrama()`](#gettrama) |
| [`html`](#html) | [`getInfo()`](#getinfo) |
| | [`getName()`](#getname) |
| | [`getEpisodes()`](#getrpisodes) |

`Anime(link)`

**Parameters**
* **link** ( [`str`](https://docs.python.org/3/library/stdtypes.html#str) ) – Link della pagina dell'anime.

## Attributes
### `link`
**Returns**
> Il **link** passato durante la creazione dell'istanza **Anime**.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### `html`
**Return**
> La **pagina** di AnimeWorld dell'anime.

**Return type**
> [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes)

## Methods
### `getTrama()`
**Return**
> La **trama** dell'anime.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### `getInfo()`
**Return**
> Un **dizionario** contenente le **informazoni** dell'anime.

**Return type**
> [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)

### `getName()`
**Return**
> Il **nome** dell'anime.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### `getEpisodes()`
**Raises**
> [`AnimeNotAvailable`](../Exceptions#class-animenotavailableexception) – Se l'anime esiste ma gli episodi non sono ancora usciti.

**Return**
> La **lista** degli **episodi** dell'anime.

**Return type**
> List[ [`Episodio`](#class-episodio) ]

***

# **class** Episodio

| [**Attributes**](#attributes-1) | [**Methods**](#methods-1) |
| :---: | :---: |
| [`number`](#number) | [`download()`](#downloadtitlenone) |
| [`links`](#links) |

## Attributes
### `number`
**Returns**
> Il **numero** dell'episodio **così com'è scritto** sulla pagina di AnimeWorld.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### `links`
**Returns**
> La **lista** di tutti i **server** in cui è ospitato l'episodio.

**Return type**
> List[ [`Server`]() ]

## Methods
### `download(title=None)`

**:warning: WARNING :warning:**
* _Scarica l'episodio nella **stessa** cartella in cui è eseguito il codice._
* _Se **NON** viene passato un titolo, il `title` sarà: `{numbero dell'episodio} - {nome del server}`._
* _**Prima** di scaricare il file il `title` viene prima sanitizzato con la funzione [`sanitize()`]()._

**Parameters**
> **title**  ( [`str`](https://docs.python.org/3/library/stdtypes.html#str) ) – Nome del file che verrà scaricato.

**Raises**
> [`ServerNotSupported`](../Exceptions#class-servernotsupportedexception) – Se l'episodio non esiste in nessun server supportato dalla libreria.

**Return**
> Ritorna `True` se l'episodio è stato scaricato altrimenti `False`.

**Return type**
> [`bool`](https://docs.python.org/3/library/functions.html#bool)