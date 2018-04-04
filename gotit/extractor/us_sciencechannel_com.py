from gotit.extractor_blueprint import us_discovery
from pprint import pprint
from multiprocessing.pool import Pool


class Extractor(us_discovery.Extractor):
    BASE_URL = "https://www.sciencechannel.com/"

    def __init__(self):
        self.NETW = "SCI"
        self.LANG = "en"
