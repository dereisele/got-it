from pluginbase import PluginBase
from pprint import pprint
import gotit
from .pipelines import ShowPipeline

class ScrapeManager(object):

    def __init__(self):

        self.extractors = {}

        self.initPlugins()
        self.initPipelines()

        self.scrapeShows()

    def initPlugins(self):
        self.plugin_base = PluginBase(package="gotit.extractors")
        self.plugin_source = self.plugin_base.make_plugin_source(
                                searchpath=["./gotit/extractor"])

        pprint(self.plugin_source.list_plugins())

    def initPipelines(self):
        self.showPip = ShowPipeline()

    def scrape(self):
        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            plugin.Extractor().extract()

    def scrapeShows(self):
        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            shows = plugin.Extractor().extractShows()
            print(plugin_name)
            for show in shows:
                self.showPip.insertShow(plugin_name, show)
                pprint(show)
