from gotit.extractor_blueprint import basic
from pprint import pprint


class Extractor(basic.Extractor):
    BASE_URL = "https://www.cbs.com"
    # Reverseengineered from CBS Android App. What is ?at=
    URL_SHOWS = "https://www.cbs.com/apps-api/v2.0/androidphone/shows/group/35.json?at=ABC11111111111111111h%2F3SQ8EUA5OQLP19LYVVZMPtObyLdtqQZm%2FhQvBPZ4ekKqY%3D"
    URL_EPISODES = "https://www.cbs.com/carousels/shows/{showId}/offset/{offset}/limit/10/"
    LANG = "en"

    def extract(self):
        show = next(self._getShows())
        pprint(show)

        episode = next(self._getEpisodes(show["x"]["x_cbs_show_id"]))
        pprint(episode)

    def extract_shows(self):
        return self._getShows()

    def _getShows(self):
        j = self.loadJson(self.URL_SHOWS)
        for show in j["group"]["showGroupItems"]:
            show_dict = {
                "name": show["title"],
                "lang": self.LANG,
                "url": show["showUrl"],
                "x": {
                    "x_cbs_show_id": show["showId"],
                }}
            yield show_dict

    def _getEpisodes(self, x_cbs_show_id):
        done = False
        offset = 0

        while not done:
            url = self.URL_EPISODES.format(showId=x_cbs_show_id, offset=offset)
            j = self.loadJson(url)

            for episode in j["result"]["data"]:
                if episode["type"] == "Full Episode":
                    episode_dict = {
                        "episode_number": episode["episode_number"],
                        "season_number": episode["season_number"],
                        "name": episode["episode_title"],
                        "url": self.BASE_URL + episode["url"],
                    }
                    yield episode_dict

            if offset + j["result"]["size"] < j["result"]["total"]:
                offset += 10
            else:
                done = True
