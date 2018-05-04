from gotit.extractor_blueprint import basic
from pprint import pprint

class Extractor(basic.Extractor):
    BASE_URL = "http://www.adultswim.com"
    URL_SHOWS = "http://www.adultswim.com/videos"
    LANG = "en"

    def extractTest(self):
        show = next(self._getShows())
        pprint(show)
        episode = next(self._getEpisodes(show["url"]))
        pprint(episode)


    def extractShows(self):
        return self._getShows()

    def extractEpisodes(self, showref):
        url = showref.url
        return self._getEpisodes(url)

    def _getShows(self):
        j = self.loadJsonViaRegex(self.URL_SHOWS, r"__AS_INITIAL_DATA__ = (.*);")
        for show in j["shows"]:
            show_dict = {
                "name": show["title"],
                "lang": self.LANG,
                "url":  self.BASE_URL + show["url"],
                "year": 0000}
            yield show_dict

    def _getEpisodes(self, showUrl):
        j = self.loadJsonViaRegex(showUrl, r"__AS_INITIAL_DATA__ = (.*);")
        for episode in j["show"]["videos"]:
            if episode["type"] == "episode":
                episode_dict = {
                    "episode_number": episode["episode_number"],
                    "season_number": episode["season_number"],
                    "name": episode["title"],
                    "url": showUrl + episode["slug"],
                    "x": {
                        "authenticated": episode["auth"],
                    }}
                yield episode_dict
