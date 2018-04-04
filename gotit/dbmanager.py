from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

base = declarative_base()

def dbConnect():
    return create_engine("sqlite:////home/alexander/gotit.db")

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
