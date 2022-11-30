import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from __main__ import logger

engine = None
Base = None
session_generator = None


def initialize(db_path):
    global engine, Base, session_generator
    try:
        engine = create_engine('sqlite:///{}'.format(db_path))
        Base = declarative_base()
        session_generator = scoped_session(sessionmaker(bind=engine))
        import ldskbkp.database.models
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.error("Could not initialize database: {}".format(e.__class__.__name__))
        raise e


def get_session_factory():
    return session_generator


def get_connection():
    return engine.connect()


def get_raw_connection():
    return engine.raw_connection()


def get_session():
    return session_generator()


def get_transaction():
    session = get_session()
    try:
        session_transaction = session.begin()
    except sqlalchemy.exc.InvalidRequestError:
        session_transaction = session.begin_nested()
    if session_transaction is None:
        raise sqlalchemy.exc.InvalidRequestError("Could not create an SQL session.")
    return session, session_transaction
