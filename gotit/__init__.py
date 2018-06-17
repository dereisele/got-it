# coding: utf-8
__version__ = '0.1'
import argparse
from .scrape import ScrapeManager


def main():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--debug", help="Start in debug mode",
                        action="store_true")
    args = parser.parse_known_args()

    if args[0].debug:
        debugMode(parser=parser)
    else:
        normalMode()


def normalMode():
    s = ScrapeManager()

    s.initPlugins()
    s.initPipelines()

    s.scrapeShows()
    s.scrapeEpisodes()


def debugMode(parser):
    s = ScrapeManager()

    print("DEBUGGING")
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-scraper", "-t-sc", help="Scraper to debug")
    parser.add_argument("--test-full", "-t-f", help="Extended testing mode",
                        action="store_true")
    parser.add_argument("--insert", "-i", help="Insert", action="store_true")
    parser.add_argument("--episodes", "-e", help="Scrape Episodes", action="store_true")
    args = parser.parse_known_args()

    if args[0].test_scraper:
        s.initPlugins()
        if args[0].test_scraper in s.extractors:
            if args[0].test_full:
                s.initPipelines()
                s.scrapeShowsOne(args[0].test_scraper, args[0].insert)
            else:
                s.testExtractor(args[0].test_scraper)
        else:
            print("Error: Scraper not found")

    if args[0].episodes:
        s.initPlugins()
        s.initPipelines()
        s.scrapeEpisodes()
