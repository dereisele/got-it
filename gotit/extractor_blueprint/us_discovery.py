from . import basic
from pprint import pprint

class Extractor(basic.Extractor):

    networks = ("SCI", "APL", "DSC")

    URL_SHOWS = "https://api.discovery.com/v1/content/shows?limit=10&networks_code={network}&offset={offset}&platform=desktop&sort=-video.airDate.type%28episode%7Climited%7Cevent%7Cstunt%7Cextra%29"
    URL_AUTH = "https://www.sciencechannel.com/anonymous?authRel=authorization&redirectUri=http%3A%2F%2Fnothing.com%3Fhttps%3A%2F%2Fwww.discovery.com"
    URL_SEASONS = "https://api.discovery.com/v1/content/seasons?excludeEmptySeasons=true&show.id={showID}"
    URL_EPISODES = "https://api.discovery.com/v1/content/videos?type=episode&season.id={seasonID}"

    def extract(self):
        self._initBearer()
        self._getShows()

    def extractShows(self):
        self._initBearer()
        return self._getShows()

    def extractEpisodes(self, showref):
        self._initBearer()
        x = self.getX(showref)
        # TODO: Ugly, but it woks
        for season in self._getSeasons(x["x_dsc_show_id"]):
            for episode in self._getEpisodes(season["x"]["x_dsc_season_id"]):
                yield episode

    def _initBearer(self):
        self.BEARER = self.loadJson(self.URL_AUTH)["access_token"]

    def _getShows(self):
        done = False
        headers = {"authorization": "Bearer " + self.BEARER}
        offset = 0

        while not done:
            url = self.URL_SHOWS.format(network=self.NETW, offset=offset)
            j = self.loadJson(url, headers=headers)

            done = not bool(j)
            offset += 10

            for show in j:
                show_dict = {
                    "name": show["name"],
                    "lang": self.LANG,
                    "url": show["socialUrl"],
                    "year": 0000,
                    "x": {
                        "x_dsc_show_id": show["id"],
                    }}
                yield show_dict

    def _getSeasons(self, x_dsc_show_id):
        headers = {"authorization": "Bearer " + self.BEARER}
        url = self.URL_SEASONS.format(showID=x_dsc_show_id)
        j = self.loadJson(url, headers=headers)

        for season in j:
            season_dict = {
                "number": season["number"],
                "name": season["name"],
                "x": {
                    "x_dsc_show_id": season["show"]["id"],
                    "x_dsc_season_id": season["id"],
                }}
            yield season_dict

    def _getEpisodes(self, x_dsc_season_id):
        headers = {"authorization": "Bearer " + self.BEARER}
        url = self.URL_EPISODES.format(seasonID=x_dsc_season_id)
        j = self.loadJson(url, headers=headers)
        for episode in j:
            #pprint(episode)
            episode_dict = {
                "episode_number": episode["episodeNumber"],
                "season_number": episode["season"]["number"],
                "name": episode["name"],
                "url": episode["socialUrl"],
                "x": {
                    "authenticated": episode["authenticated"],
                    "x_dsc_show_id": episode["show"]["id"],
                    "x_dsc_season_id": episode["season"]["id"],
                    "x_dsc_episode_id": episode["id"],
                }}
            yield episode_dict
