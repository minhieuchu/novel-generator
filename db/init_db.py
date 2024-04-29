import os
from sqlalchemy import create_engine

from db.base_class import Base
from db import base

POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST", "localhost")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT", 5432)
POSTGRESQL_USERNAME = os.getenv("POSTGRESQL_USERNAME", "postgres")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "LuiCsf5LUikmnI7TGR")
POSTGRESQL_DBNAME = os.getenv("POSTGRESQL_DBNAME", "ai_novel_generator")
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DBNAME}"

sql_alchemy_engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


def initialize_database_tables() -> bool:
    Base.metadata.create_all(bind=sql_alchemy_engine)
    return True


def clear_database_tables() -> bool:
    Base.metadata.drop_all(bind=sql_alchemy_engine)
    return True
