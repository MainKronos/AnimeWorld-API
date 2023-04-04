import unittest

import animeworld as aw

anime_link = "https://www.animeworld.tv/play/summertime-render.GDU38"




class TestAnimeWorld(unittest.TestCase):
	def setUp(self):
		self.anime = aw.Anime(link=anime_link)

	def test_Anime(self):

		with self.subTest(msg="Anime"):
			self.assertIsInstance(self.anime, aw.Anime)

		with self.subTest(msg="getName"):
			self.assertIsInstance(self.anime.getName(), str)
		
		with self.subTest(msg="getTrama"):
			self.assertIsInstance(self.anime.getTrama(), str)
		
		with self.subTest(msg="getInfo"):
			self.assertIsInstance(self.anime.getInfo(), dict)
		
	# def test_Episodio(self):	
	# 	episodi = self.anime.getEpisodes()



if __name__ == '__main__':
    unittest.main()