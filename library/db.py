from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import Config

DATABASE_URL = URL.create(
    drivername='postgresql+psycopg2',
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    username=Config.DB_USER,
    password=Config.DB_PASS,
    database=Config.DB_NAME
)
engine = create_engine(url=DATABASE_URL)
Base = declarative_base()
LocalSession = sessionmaker(engine)


def get_db():
    return LocalSession()
