from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from MetaButler import DB_URI, MInit, log


def start() -> scoped_session:
    if DB_URI.startswith("sqlite"):
        engine = create_engine(DB_URI, echo=MInit.DEBUG)
    else:
        engine = create_engine(DB_URI, client_encoding="utf8", echo=MInit.DEBUG)
    log.info(f"Connecting to database ({DB_URI.split('://')[0]})......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))



BASE = declarative_base()
try:
    SESSION: scoped_session = start()
except Exception as e:
    log.exception(f'[PostgreSQL] Failed to connect due to {e}')
    exit()
   
log.info("[PostgreSQL] Connection successful, session started.")
