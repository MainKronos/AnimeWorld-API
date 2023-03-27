import animeworld as aw
from datetime import datetime


def my_hook(d):
	"""
	Stampa una ProgressBar con tutte le informazioni di download.
	"""
	if d['status'] == 'downloading':
		out = "{filename}:\n[{bar}][{percentage:^6.1%}]\n{downloaded_bytes}/{total_bytes} in {elapsed:%H:%M:%S} (ETA: {eta:%H:%M:%S})\x1B[3A"

		width = 70 # grandezza progressbar

		d['elapsed'] = datetime.utcfromtimestamp(d['elapsed'])
		d['eta'] = datetime.utcfromtimestamp(d['eta'])
		d['bar'] = '#'*int(width*d['percentage']) + ' '*(width-int(width*d['percentage']))

		print(out.format(**d))

	elif d['status'] == 'finished':
		print('\n\n\n')


try:
	anime = aw.Anime(link="https://www.animeworld.tv/play/tokyo-revengers-seiya-kessen-hen.tzgly")
	
	print("Titolo:", anime.getName()) # Titolo dell'anime

	print("\n----------------------------------\n")

	print("Trama:", anime.getTrama()) # Trama

	print("\n----------------------------------\n")

	print("Info:")
	info = anime.getInfo()
	for x in info: print(f"{x}: {info[x]}") # Informazioni presenti su Animeworld riguardanti l'anime

	print("\n----------------------------------\n")

	print("Episodi:")
	try:
		episodi = anime.getEpisodes()
	except aw.AnimeNotAvailable as error:
		print("Errore:", error)
	else:
		for x in episodi:
			print(f"\n-> Ep. {x.number}")
			for k in x.links:
				print(f"\t{k.name} - {k.link}")

			if x.number == '1':
				print("\n\tFile info: {\n\t\t" + "\n\t\t".join("{}: {}".format(k, v) for k, v in x.fileInfo().items()) + "\n\t}")
				x.download(hook=my_hook)
				break
except (aw.DeprecatedLibrary, aw.Error404, aw.ServerNotSupported) as error:
	print(error)
