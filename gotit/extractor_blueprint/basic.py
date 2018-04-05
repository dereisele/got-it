import requests
import json


class Extractor(object):
    def extract(self):
        raise NotImplementedError

    def extractShows(self):
        raise NotImplementedError

    def extractEpisodes(self, showref):
        raise NotImplementedError

    def loadJson(self, url, **kwargs):
        r = requests.get(url, **kwargs)
        j = json.loads(r.text)
        return j

    def getX(self, object):
        """Get x attribute from show as dict."""
        return json.loads(object.x)
