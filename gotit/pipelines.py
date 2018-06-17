from sqlalchemy.orm import sessionmaker
from json import dumps
from .dbmanager import dbConnect, createTables, get_or_create
from .models import Show, Scraper, ShowScraperRef, Season, Episode, EpisodeScraperRef


class ShowPipeline(object):
    def __init__(self):
        engine = dbConnect()
        createTables(engine)
        self.Session = sessionmaker(bind=engine)()

    def insertShow(self, scraper_id, show):
        dbShow, _ = get_or_create(self.Session, Show,
                                  name=show["name"],
                                  year=show["year"],
                                  lang=show["lang"])

        dbScraper, _ = get_or_create(self.Session, Scraper, string_id=scraper_id)

        get_or_create(self.Session, ShowScraperRef,
                      scraper_id=dbScraper.id,
                      show_id=dbShow.id,
                      x=dumps(show.get("x")),
                      url=show["url"])

    def insertEpisode(self, showref, episode):
        dbSeason, _ = get_or_create(self.Session, Season,
                                    number=episode["season_number"],
                                    show_id=showref.show_id)

        dbEpisode, _ = get_or_create(self.Session, Episode,
                                     season_id=dbSeason.id,
                                     number=episode["episode_number"],
                                     name=episode["name"])

        get_or_create(self.Session, EpisodeScraperRef,
                      episode_id=dbEpisode.id,
                      scraper_id=showref.scraper_id,
                      url=episode["url"],
                      x=dumps(episode.get("x")))

    def __del__(self):
        try:
            self.Session.close()
        except AttributeError:
            pass
