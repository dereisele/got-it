from gotit.extractor_blueprint import basic
from pprint import pprint


class Extractor(basic.Extractor):
    BASE_URL = "https://www.funk.net/"
    URL_SHOWS = "https://www.funk.net/api/v3.0/content/channels/?size=100"
    URL_SHOW = "https://www.funk.net/channel/{alias}"
    URL_SEASONS = "https://www.funk.net/api/v3.0/content/playlists/filter/?channelId={alias}&secondarySort=alias,ASC"
    URL_EPISODES = "https://www.funk.net/api/v3.0/content/playlists/{alias}/videos/?size=100&secondarySort=episodeNr,ASC"
    URL_EPISODE = "https://www.funk.net/channel/{showAlias}/{episodeAlias}/{seasonAlias}/"
    LANG = "de"

    def extract(self):
        show = next(self._getShows())
        pprint(show)
        season = next(self._getSeasons(show["x"]["x_funk_show_alias"]))
        pprint(season)
        episode = next(self._getEpisodes(season["x"]["x_funk_season_alias"]))
        pprint(episode)

    def extract_shows(self):
        return self._getShows()

    def _getShows(self):
        j = self.loadJson(self.URL_SHOWS)
        for show in j["result"]:
            if show["type"] == "Series":
                show_dict = {
                    "name": show["title"],
                    "lang": self.LANG,
                    "url": self.URL_SHOW.format(alias=show["alias"]),
                    "x": {
                        "x_funk_show_alias": show["alias"],
                    }}
                yield show_dict

    def _getSeasons(self, x_funk_show_alias):
        url = self.URL_SEASONS.format(alias=x_funk_show_alias)
        j = self.loadJson(url)

        alias = j["parentResult"]["alias"]

        for season in j["result"]:
            ov = "(OV)" in season["title"]
            number = season["alias"].split("staffel-")[1]
            season_dict = {
                "number": number,
                "name": season["title"],
                "x": {
                    "x_funk_show_alias": alias,
                    "x_funk_season_alias": season["alias"],
                    "x_funk_ov": ov,
                }}
            yield season_dict

    def _getEpisodes(self, x_funk_season_alias):
        url = self.URL_EPISODES.format(alias=x_funk_season_alias)
        j = self.loadJson(url)

        seasonAlias = j["parentResult"]["alias"]
        showAlias = seasonAlias.split("-staffel")[0]

        for episode in j["result"]:
            episode_dict = {
                "number": episode["episodeNr"],
                "name": episode["title"],
                "url": self.URL_EPISODE.format(
                    showAlias=showAlias,
                    seasonAlias=seasonAlias,
                    episodeAlias=episode["alias"]),
                "x": {
                    "x_funk_show_alias": showAlias,
                    "x_funk_season_alias": seasonAlias,
                    "x_funk_episode_alias": episode["alias"],
                }}
            yield episode_dict
