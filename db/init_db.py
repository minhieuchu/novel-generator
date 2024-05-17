import os
import motor.motor_asyncio
from sqlalchemy import create_engine

from db.base_class import Base
from db import base

# PostgreSQL
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST", "localhost")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT", 5432)
POSTGRESQL_USERNAME = os.getenv("POSTGRESQL_USERNAME", "postgres")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "LuiCsf5LUikmnI7TGR")
POSTGRESQL_DBNAME = os.getenv("POSTGRESQL_DBNAME", "ai_novel_generator")
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DBNAME}"

sql_alchemy_engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# MongoDB
MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "F4NB1oPmM60eKHH")
MONGO_DETAILS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017"
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
mongo_database = mongo_client.novel_generator


def initialize_postgres_database() -> bool:
    Base.metadata.create_all(bind=sql_alchemy_engine)
    return True


def clear_postgres_database() -> bool:
    Base.metadata.drop_all(bind=sql_alchemy_engine)
    return True


async def initialize_mongodb():
    await mongo_database.get_collection("stories").create_index({"title": 1})
