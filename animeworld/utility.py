"""
Modulo per delle funzioni di utilità.
"""
import requests
from bs4 import BeautifulSoup
import inspect
from typing import *

from .globals import HDR, cookies
from .exceptions import DeprecatedLibrary


def HealthCheck(fun):
	"""
	Controlla se la libreria è deprecata
	"""
	def wrapper(*args, **kwargs):
		try:
			return fun(*args, **kwargs)
		except AttributeError:
			frame = inspect.trace()[-1]
			funName = frame[3]
			errLine = frame[2]
			raise DeprecatedLibrary(funName, errLine)
	return wrapper

@HealthCheck
def find(keyword: str) -> Optional[Dict]:
	"""
	Ricerca un anime tramite le API interne di Animeworld.

	- `keyword`: Il nome dell'anime o una porzione di esso.

	```
	return {
	  name: str, # Nome dell'anime trovato
	  link: str # Link dell'anime trovato
	}
	```
	"""
	res = requests.get("https://www.animeworld.tv", headers = HDR)
	cookies.update(res.cookies.get_dict())
	soupeddata = BeautifulSoup(res.content, "html.parser")
	myHDR = {"csrf-token": soupeddata.find('meta', {'id': 'csrf-token'}).get('content')}


	res = requests.post("https://www.animeworld.tv/api/search/v2?", params = {"keyword": keyword} ,headers=myHDR, cookies=cookies)

	data = res.json()["animes"]
	data.sort(key=lambda a: a["dub"])

	# with open("index.html", 'w') as f:
	# 	json.dump(data, f, indent='\t')


	if len(data) == 0:
		return None
	else:
		return {
			"name": data[0]["name"],
			"link": f"https://www.animeworld.tv/play/{data[0]['link']}.{data[0]['identifier']}"
		}