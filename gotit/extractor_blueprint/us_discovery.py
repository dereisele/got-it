from . import basic

class Extractor(basic.Extractor):


    networks= ("SCI", "APL", "DSC")

    URL_SHOWS = "https://api.discovery.com/v1/content/shows?limit=10&networks_code={network}&offset={offset}&platform=desktop&sort=-video.airDate.type%28episode%7Climited%7Cevent%7Cstunt%7Cextra%29"
    URL_AUTH = "https://www.sciencechannel.com/anonymous?authRel=authorization&redirectUri=http%3A%2F%2Fnothing.com%3Fhttps%3A%2F%2Fwww.discovery.com"
    URL_SEASONS = "https://api.discovery.com/v1/content/seasons?excludeEmptySeasons=true&show.id={showID}"
    URL_EPISODES = "https://api.discovery.com/v1/content/videos?type=episode&season.id={seasonID}"

    def extract(self):
        self._initBearer()
        self._getShows()

    def extractShows(self):
        self._initBearer()
        self._getShows()

    def _initBearer(self):
        self.BEARER = self.loadJson(self.URL_AUTH)["access_token"]

    def _getShows(self):
        done = False
        #shows = []
        headers = {"authorization": "Bearer " + self.BEARER}
        offset = 0

        while not done:
            url = self.URL_SHOWS.format(network=self.NETW, offset=offset)
            j = self.loadJson(url, headers=headers)

            done = not bool(j)
            offset += 10

            for show in j:
                show_dict = {
                            "title": show["name"],
                            "lang": self.LANG,
                            "x-disc-show-id": show["id"],
                            }
                yield show_dict
                #shows.append(show_dict)

        #return(shows)

    def _getSeasons(self, show):
        headers = {"authorization": "Bearer " + self.BEARER}
        url = self.URL_SEASONS.format(showID=show["x-disc-show-id"])
        j = self.loadJson(url, headers=headers)
        return j
