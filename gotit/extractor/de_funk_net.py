from gotit.extractor_blueprint import basic
from pprint import pprint


class Extractor(basic.Extractor):
    BASE_URL = "https://www.funk.net/"
    URL_SHOWS = "https://www.funk.net/api/v3.0/content/channels/?size=100"
    URL_SHOW = "https://www.funk.net/channel/{alias}"
    URL_SEASONS = "https://www.funk.net/api/v3.0/content/playlists/filter/?channelId={alias}&secondarySort=alias,ASC"
    URL_EPISODES = "https://www.funk.net/api/v3.0/content/playlists/{alias}/videos/?size=100&secondarySort=episodeNr,ASC"
    URL_EPISODE = "https://www.funk.net/channel/{showAlias}/{episodeAlias}/{seasonAlias}/"
    headers = {"authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnROYW1lIjoiY3VyYXRpb24tdG9vbCIsInNjb3BlIjoic3RhdGljLWNvbnRlbnQtYXBpLGN1cmF0aW9uLWFwaSxzZWFyY2gtYXBpIn0.q4Y2xZG8PFHai24-4Pjx2gym9RmJejtmK6lMXP5wAgc"}
    LANG = "de"

    def extract(self):
        show = next(self._getShows())
        pprint(show)
        season = next(self._getSeasons(show["x"]["x_funk_show_alias"]))
        pprint(season)
        episode = next(self._getEpisodes(season["x"]["x_funk_season_alias"]))
        pprint(episode)

    def extractShows(self):
        return self._getShows()

    def extractEpisodes(self, showref):
        x = self.getX(showref)
        # TODO: Ugly, but it woks
        for season in self._getSeasons(x["x_funk_show_alias"]):
            for episode in self._getEpisodes(season["x"]["x_funk_season_alias"]):
                yield episode

    def _getShows(self):
        j = self.loadJson(self.URL_SHOWS)
        for show in j["result"]:
            if show["type"] == "Series":
                show_dict = {
                    "name": show["title"],
                    "lang": self.LANG,
                    "url": self.URL_SHOW.format(alias=show["alias"]),
                    "year": 0000,
                    "x": {
                        "x_funk_show_alias": show["alias"],
                    }}
                yield show_dict

    def _getSeasons(self, x_funk_show_alias):
        url = self.URL_SEASONS.format(alias=x_funk_show_alias)
        j = self.loadJson(url, headers=self.headers)

        alias = j["parentResult"]["alias"]

        if not j["result"]:
            return

        for season in j["result"]:
            ov = "(OV)" in season["title"]
            try:
                number = season["alias"].split("staffel-")[1]
            except(IndexError):
                number = 0  # For extras
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
        j = self.loadJson(url, headers=self.headers)

        season_alias = j["parentResult"]["alias"]
        show_alias = season_alias.split("-staffel")[0]

        if not j["result"]:
            return  # YES, there are also empty seasons

        for episode in j["result"]:
            pprint(episode)
            episode_dict = {
                "episode_number": episode["episodeNr"],
                "season_number": episode["seasonNr"],
                "name": episode["title"],
                "url": self.URL_EPISODE.format(
                    showAlias=show_alias,
                    seasonAlias=season_alias,
                    episodeAlias=episode["alias"]),
                "x": {
                    "x_funk_show_alias": show_alias,
                    "x_funk_season_alias": season_alias,
                    "x_funk_episode_alias": episode["alias"],
                }}
            yield episode_dict
