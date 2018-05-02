from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
    scraper = relationship("Scraper")
    url = Column(String)
    x = Column(String)


class Season(base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    show = relationship("Show")
    number = Column(Integer)
    name = Column(String)


class Episode(base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.id"))
    season = relationship("Season")
    number = Column(Integer)
    name = Column(String)
    x = Column(String)


class EpisodeScraperRef(base):
    __tablename__ = "episode_scraper_ref"
    id = Column(Integer, primary_key=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"))
    scraper_id = Column(Integer, ForeignKey("scrapers.id"))
    scraper = relationship("Scraper")
    url = Column(String)
    x = Column(String)
