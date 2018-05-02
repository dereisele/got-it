from sqlalchemy.orm import sessionmaker
from json import dumps
from .dbmanager import dbConnect, createTables, get_or_create
from .models import Show, Scraper, ShowScraperRef, Season, Episode, EpisodeScraperRef


class ShowPipeline(object):
    def __init__(self):
        engine = dbConnect()
        createTables(engine)
        self.Session = sessionmaker(bind=engine)

    def insertShow(self, scraper_id, show):
        session = self.Session()

        dbShow, _ = get_or_create(session, Show,
                                  name=show["name"],
                                  year=show["year"],
                                  lang=show["lang"])

        dbScraper, _ = get_or_create(session, Scraper, string_id=scraper_id)

        get_or_create(session, ShowScraperRef,
                      scraper_id=dbScraper.id,
                      show_id=dbShow.id,
                      x=dumps(show["x"]),
                      url=show["url"])

    def insertEpisode(self, showref, episode):
        session = self.Session()

        dbSeason, _ = get_or_create(session, Season,
                                    number=episode["season_number"],
                                    show_id=showref.show_id)

        dbEpisode, _ = get_or_create(session, Episode,
                                     season_id=dbSeason.id,
                                     number=episode["episode_number"],
                                     name=episode["name"])

        get_or_create(session, EpisodeScraperRef,
                      episode_id=dbEpisode.id,
                      scraper_id=showref.scraper_id,
                      url=episode["url"],
                      x=dumps(episode["x"]))
