import requests
import json
class Extractor(object):
    def extract(self):
        raise NotImplementedError

    def loadJson(self, url, **kwargs):
        r = requests.get(url, **kwargs)
        j = json.loads(r.text)
        return j
