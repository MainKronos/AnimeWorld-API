# **class** ServerNotSupported(_Exception_)
_Viene sollevata questa eccezione quando si tenta di scaricare un episodio ospitato su un server non supportato dalla libreria._

## Attributes
### `server`
**Returns**
> Il **nome** del server non supportato.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### `message`
**Returns**
> Il **messaggio** di errore.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

# **class** AnimeNotAvailable(_Exception_)
_Viene sollevata questa eccezione quando la serie non è ancora uscita, cioè non esistono ancora gli episodi dell'anime._

## Attributes
### `anime`
**Returns**
> Il **nome** dell'anime.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### `message`
**Returns**
> Il **messaggio** di errore.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

# **class** DeprecatedLibrary(_Exception_)
_Viene sollevata questa eccezione quando il sito AnimeWorld ha subito dei mutamenti nei punti dove la libreria opera._

## Attributes
### `funName`
**Returns**
> Il **nome** della funzione dove è sorto l'errore.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)

### `line`
**Returns**
> La **linea** dove è sorto l'errore.

**Return type**
> [`int`](https://docs.python.org/3/library/functions.html#int)

### `message`
**Returns**
> Il **messaggio** di errore.

**Return type**
> [`str`](https://docs.python.org/3/library/stdtypes.html#str)