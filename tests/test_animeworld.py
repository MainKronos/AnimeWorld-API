import unittest

import unittest
import random, io, time
from threading import Thread

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
    ep = random.choice(aw.Anime("https://www.animeworld.so/play/fullmetal-alchemist-brotherhood.4vGGQ").getEpisodes())

    server = [s for s in ep.links if s.Nid == 2][0]

    with self.assertRaises(aw.ServerNotSupported):
      server.fileLink()


class TestAnimeWorld(unittest.TestCase):
  @classmethod
  def setUpClass(cls) -> None:
    """Inizializza la classe Anime."""
    cls.anime = aw.Anime("https://www.animeworld.so/play/fullmetal-alchemist-brotherhood.4vGGQ")

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

  def test_episodio(self):
    ep = random.choice(self.anime.getEpisodes())

    self.assertIsInstance(ep, aw.Episodio)
    self.assertIsInstance(ep.number, str)
    self.assertIsInstance(ep.links, list)

class TestServer(unittest.TestCase):
  @classmethod
  def setUpClass(cls) -> None:
    """Sceglie un episodio per i test."""
    cls.episodio = random.choice(aw.Anime("https://www.animeworld.so/play/fullmetal-alchemist-brotherhood.4vGGQ").getEpisodes())
  
  @staticmethod
  def stopDownload(opt:list):
    time.sleep(1)
    opt.append("abort")
  
  def test_AnimeWorld_Server(self) -> None:

    servers = [e for e in self.episodio.links if isinstance(e, AnimeWorld_Server)]

    if len(servers) == 0:
      self.skipTest('Il server AnimeWorld_Server non esiste in questo episodio.')
      return
    
    server = servers[0]

    self.assertEqual(server.Nid, 9)
    self.assertEqual(server.name, "AnimeWorld Server")
    self.assertIsInstance(server.fileLink(), str)

    info = server.fileInfo()
    self.assertIsInstance(info, dict)
    self.assertIn("content_type", info)
    self.assertIn("total_bytes", info)
    self.assertIn("last_modified", info)
    self.assertIn("server_name", info)
    self.assertIn("server_id", info)
    self.assertIn("url", info)

    with self.subTest('Animeworld_Server Download'):
      buf = io.BytesIO()
      opt = []
      Thread(target=self.stopDownload, args=(opt,)).start()
      self.assertIsNone(server.download(folder=buf, opt=opt))
      buf.close()

  def test_Streamtape(self) -> None:
    servers = [e for e in self.episodio.links if isinstance(e, Streamtape)]

    if len(servers) == 0:
      self.skipTest('Il server Streamtape non esiste in questo episodio.')
      return
    
    server = servers[0]
    
    self.assertEqual(server.Nid, 8)
    self.assertEqual(server.name, "Streamtape")

    
    self.assertIsInstance(server.fileLink(), str)    

    info = server.fileInfo()
    self.assertIsInstance(info, dict)
    self.assertIn("content_type", info)
    self.assertIn("total_bytes", info)
    self.assertIn("last_modified", info)
    self.assertIn("server_name", info)
    self.assertIn("server_id", info)
    self.assertIn("url", info)

    with self.subTest('Streamtape Download'):
      buf = io.BytesIO()
      opt = []
      Thread(target=self.stopDownload, args=(opt,)).start()
      self.assertIsNone(server.download(folder=buf, opt=opt))
      buf.close()

if __name__ == '__main__':
  unittest.main(verbosity=2)