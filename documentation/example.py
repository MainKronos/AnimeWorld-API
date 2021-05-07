import animeworld as aw

def main():


	try:
		anime = aw.Anime(link="https://www.animeworld.tv/play/jaku-chara-tomozaki-kun.RDPHq")
		
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
		except (aw.ServerNotSupported, aw.AnimeNotAvailable) as error:
			print("Errore:", error)
		else:
			for x in episodi:
				print(f"\n-> Ep. {x.number}")
				for k in x.links:
					print(f"\t{k.name} - {k.link}")

				# if x.number == '4':
				# 	x.download()
	except aw.DeprecatedLibrary as error:
		print(error)

if __name__ == '__main__':
	main()