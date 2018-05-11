from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

base = declarative_base()

from .models import Show, ShowScraperRef, Scraper

def dbConnect():
    return create_engine("mysql+mysqlconnector://python:python-passwd@localhost/python")

def createTables(engine):
    base.metadata.create_all(engine)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True

def getShows():
    engine = dbConnect()
    createTables(engine)
    session = sessionmaker(bind=engine)()
    shows = session.query(Show)
    session.close()
    return shows


def getShowScraperRef(ignore_filter=False):
    engine = dbConnect()
    createTables(engine)
    session = sessionmaker(bind=engine)()

    # TODO: for early debugging
    if ignore_filter:
        show_scraper_refs = session.query(ShowScraperRef)
    else:
        scraper_string = input("scraper_string: ")
        scraper_id = session.query(Scraper).filter_by(string_id=scraper_string).first().id
        show_scraper_refs = session.query(ShowScraperRef).filter_by(scraper_id=scraper_id)
    session.close()
    return show_scraper_refs
