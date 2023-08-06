import unittest

import unittest
import random

import animeworld as aw
from animeworld.servers import AnimeWorld_Server, Streamtape

class TestGeneral(unittest.TestCase):
  def test_find(self):
    """
    Testa la funzione find.
    """
    res = aw.find("Sabikui Bisco 2")

    self.assertIsInstance(res, list)
    self.assertGreater(len(res), 0)

    anime = random.choice(res)

    self.assertIsInstance(anime, dict)

    self.assertIn("id", anime)
    self.assertIn("name", anime)
    self.assertIn("jtitle", anime)
    self.assertIn("studio", anime)
    self.assertIn("release", anime)
    self.assertIn("episodes", anime)
    self.assertIn("state", anime)
    self.assertIn("story", anime)
    self.assertIn("categories", anime)
    self.assertIn("image", anime)
    self.assertIn("durationEpisodes", anime)
    self.assertIn("link", anime)
    self.assertIn("createdAt", anime)
    self.assertIn("language", anime)
    self.assertIn("year", anime)
    self.assertIn("dub", anime)
    self.assertIn("season", anime)
    self.assertIn("totViews", anime)
    self.assertIn("dayViews", anime)
    self.assertIn("weekViews", anime)
    self.assertIn("monthViews", anime)
    self.assertIn("malId", anime)
    self.assertIn("anilistId", anime)
    self.assertIn("mangaworldId", anime)
    self.assertIn("malVote", anime)
    self.assertIn("trailer", anime)

    self.fail("Test")

class TestExceptions(unittest.TestCase):
  def test_Error404(self) -> None:
    """
    Testa il corretto riconoscimento di una pagina 404.
    """
    with self.assertRaises(aw.Error404):
      aw.Anime("https://www.animeworld.so/play/ttt")

  # @unittest.skip("Link da aggiornare con uno non ancora disponibile.")
  def test_AnimeNotAvailable(self) -> None:
    """
    Testa il corretto riconoscimento di un anime non ancora disponibile.
    """
    res = aw.Anime("https://www.animeworld.so/play/sabikui-bisco-2.6CCbU")

    with self.assertRaises(aw.AnimeNotAvailable):
      res.getEpisodes()
  
  def test_ServerNotSupported(self) -> None:
    """
    Testa il corretto riconoscimento di un server non supportato.
    """
    ep = random.choice(aw.Anime("https://www.animeworld.so/play/fullmetal-alchemist-brotherhood.Ihtnf").getEpisodes())

    server = [s for s in ep.links if s.Nid == 2][0]

    with self.assertRaises(aw.ServerNotSupported):
      server.fileLink()


class TestAnimeWorld(unittest.TestCase):
  @classmethod
  def setUpClass(cls) -> None:
    """Inizializza la classe Anime."""
    cls.anime = aw.Anime("https://www.animeworld.so/play/fullmetal-alchemist-brotherhood.Ihtnf")

  def test_anime(self):
    """
    Testa l'ottenimento delle informazioni relative all'anime.
    """
    self.assertIsInstance(self.anime.getName(), str)
    self.assertIsInstance(self.anime.getTrama(), str)

    info = self.anime.getInfo()
    self.assertIsInstance(info, dict)
    self.assertIn('Categoria', info)
    self.assertIn('Audio', info)
    self.assertIn('Data di Uscita', info)
    self.assertIn('Stagione', info)
    self.assertIn('Studio', info)
    self.assertIn('Genere', info)
    self.assertIn('Voto', info)
    self.assertIn('Durata', info)
    self.assertIn('Episodi', info)
    self.assertIn('Stato', info)
    self.assertIn('Visualizzazioni', info)

  def test_servers(self):
    """
    Controlli relativi ai server.
    """
    ep = random.choice(self.anime.getEpisodes())

    servers = ep.links

    animeworld_server = [e for e in servers if isinstance(e, AnimeWorld_Server)][0]
    streamtape_server = [e for e in servers if isinstance(e, Streamtape)][0]

    self.assertEqual(animeworld_server.Nid, 9)
    self.assertEqual(animeworld_server.name, "AnimeWorld Server")

    self.assertEqual(streamtape_server.Nid, 8)
    self.assertEqual(streamtape_server.name, "Streamtape")

    self.assertIsInstance(animeworld_server.fileLink(), str)
    self.assertIsInstance(streamtape_server.fileLink(), str)

    animeworld_info = animeworld_server.fileInfo()
    self.assertIsInstance(animeworld_info, dict)
    self.assertIn("content_type", animeworld_info)
    self.assertIn("total_bytes", animeworld_info)
    self.assertIn("last_modified", animeworld_info)
    self.assertIn("server_name", animeworld_info)
    self.assertIn("server_id", animeworld_info)
    self.assertIn("url", animeworld_info)

    streamtape_info = streamtape_server.fileInfo()
    self.assertIsInstance(animeworld_info, dict)
    self.assertIn("content_type", streamtape_info)
    self.assertIn("total_bytes", streamtape_info)
    self.assertIn("last_modified", streamtape_info)
    self.assertIn("server_name", streamtape_info)
    self.assertIn("server_id", streamtape_info)
    self.assertIn("url", streamtape_info)

if __name__ == '__main__':
  unittest.main(verbosity=2)