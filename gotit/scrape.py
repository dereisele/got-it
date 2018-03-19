from pluginbase import PluginBase
from pprint import pprint

class ScrapeManager(object):

    def __init__(self):

        self.extractors = {}

        self.initPlugins()

    def initPlugins(self):
        self.plugin_base = PluginBase(package="gotit.extractors")
        self.plugin_source = self.plugin_base.make_plugin_source(
                                searchpath=["./gotit/extractor"])

        pprint(self.plugin_source.list_plugins())

        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            plugin.Extractor().extract()
