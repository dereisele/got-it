from gotit.extractor_blueprint import basic
from pprint import pprint
from string import ascii_uppercase

class Extractor(basic.Extractor):
    BASE_URL = "https://www.zdf.de/"
    URL_SHOWS = "https://www.zdf.de/sendungen-a-z?group={letter}"
    LANG = "de"

    def extractTest(self):
        show = next(self._getShows())
        pprint(show)
        #episode = next(self._getEpisodes(show["url"]))
        #pprint(episode)

    def extractShows(self):
        return []
        return [next(self._getShows())]

    def extractEpisodes(self, showref):
        return []
        url = showref.url
        return self._getEpisodes(url)

    def _getShows(self):
        for l in (*ascii_uppercase, "0+-+9"):
            url = self.URL_SHOWS.format(letter=l)
            shows = self.loadRegex(url, r"data-plusbar-title=\"(.*)\"\s+data-plusbar-twitter-title=\".*\"\s+data-plusbar-url=\"(.*)\"")

            for title, url in shows:
                show_dict = {
                    "name": title,
                    "lang": self.LANG,
                    "url":  url,
                    "year": 0000}
                yield show_dict

    def _getEpisodes(self, url):
        pass
