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