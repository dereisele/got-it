from gotit.extractor_blueprint import basic
import requests
import re

class Extractor(basic.Extractor):
    BASE_URL = "https://www.funk.net/"

    def extract(self):
        print("test")

    def extract_shows(self):
        site = requests.get(BASE_URL).text()
