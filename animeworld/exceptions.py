"""
Modulo per le eccezioni.
"""


class ServerNotSupported(Exception):
	"""Il server da dove si tenta di scaricare l'episodio non è supportato."""
	def __init__(self, server):
		self.server = server
		self.message = f"Il server {server} non è supportato."
		super().__init__(self.message)

class AnimeNotAvailable(Exception):
	"""L'anime non è ancora disponibile."""
	def __init__(self, animeName=''):
		self.anime = animeName
		self.message = f"L'anime '{animeName}' non è ancora disponibile."
		super().__init__(self.message)

class Error404(Exception):
	"""Il link porta ad una pagina inesistente."""
	def __init__(self, link):
		self.link = link
		self.message = f"Il link '{link}' porta ad una pagina inesistente."
		super().__init__(self.message)

class DeprecatedLibrary(Exception):
	"""Libreria deprecata a causa di un cambiamento della struttura del sito."""
	def __init__(self, file, funName, line):
		self.funName = funName
		self.line = line
		self.message = f"Il sito è cambiato, di conseguenza la libreria è DEPRECATA. -> [File {file} in {funName} - {line}]"
		super().__init__(self.message)

class HardStoppedDownload(Exception):
	"""Il file in download è stato forsatamente interrotto."""
	def __init__(self):
		self.message = "Il file in download è stato forsatamente interrotto."
		super().__init__(self.message)