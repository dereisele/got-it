from gotit.extractor_blueprint import us_discovery
from pprint import pprint
from multiprocessing.pool import Pool


class Extractor(us_discovery.Extractor):
    BASE_URL = "https://www.sciencechannel.com/"

    def __init__(self):
        self.NETW = "SCI"
        self.LANG = "en"

    def extract(self):
        self._initBearer()

        """
        with Pool(1) as p:
            rst = p.map(self._getSeasons, self._getShows())
            pprint(rst)
        """
        show = next(self._getShows())
        season = next(self._getSeasons(show["x"]["x_dsc_show_id"]))
        episode = next(self._getEpisodes(season["x"]["x_dsc_season_id"]))
        pprint(episode)
