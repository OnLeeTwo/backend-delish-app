from sqlalchemy import create_engine
from config.config import Config


def connect_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    connection = engine.connect()

    return connection
