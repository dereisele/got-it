import requests
import json
import re


class Extractor(object):
    def extractTest(self):
        raise NotImplementedError

    def extractShows(self):
        raise NotImplementedError

    def extractEpisodes(self, showref):
        raise NotImplementedError

    def loadJson(self, url, **kwargs):
        r = requests.get(url, **kwargs)
        j = json.loads(r.text)
        return j

    def loadJsonViaRegex(self, url, patern, **kwargs):
        r = requests.get(url, **kwargs)
        reg = re.findall(patern, r.text)[0]
        j = json.loads(reg)
        return j

    def getX(self, object):
        """Get x attribute from show as dict."""
        return json.loads(object.x)
