from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .dbmanager import base


class Show(base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    year = Column(Integer, nullable=True)
    lang = Column(String(8))


class Scraper(base):
    __tablename__ = "scrapers"
    id = Column(Integer, primary_key=True)
    string_id = Column(String(32))


class ShowScraperRef(base):
    __tablename__ = "show_scraper_ref"
    id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    scraper_id = Column(Integer, ForeignKey("scrapers.id"))
    scraper = relationship("Scraper")
    url = Column(String(96))
    x = Column(String(64))


class Season(base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    show = relationship("Show")
    number = Column(Integer)
    name = Column(String(32))


class Episode(base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.id"))
    season = relationship("Season")
    number = Column(Integer)
    name = Column(String(32))
    x = Column(String(64))


class EpisodeScraperRef(base):
    __tablename__ = "episode_scraper_ref"
    id = Column(Integer, primary_key=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"))
    scraper_id = Column(Integer, ForeignKey("scrapers.id"))
    scraper = relationship("Scraper")
    url = Column(String(96))
    x = Column(String(64))
