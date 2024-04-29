from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from db.init_db import sql_alchemy_engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sql_alchemy_engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
