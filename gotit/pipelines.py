from sqlalchemy.orm import sessionmaker
from json import dumps
from .dbmanager import dbConnect, createTables, get_or_create
from .models import Show, Scraper, ShowScraperRef


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
