from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .dbmanager import base


class Show(base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer, nullable=True)
    lang = Column(String)


class Scraper(base):
    __tablename__ = "scrapers"
    id = Column(Integer, primary_key=True)
    string_id = Column(String)


class ShowScraperRef(base):
    __tablename__ = "show_scraper_ref"
    id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    scraper_id = Column(Integer, ForeignKey("scrapers.id"))
    url = Column(String)
    x = Column(String)
