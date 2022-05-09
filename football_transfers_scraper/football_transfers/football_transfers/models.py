import datetime
import logging
from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
    Integer,
    VARCHAR,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from football_transfers.settings import DATABASE


logger = logging.getLogger()


DeclarativeBase = declarative_base()


def connect_db():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """

    return create_engine(URL(**DATABASE))


class FutureStar(DeclarativeBase):
    """
    Sqlalchemy model for future_star table
    """

    __tablename__ = "future_star"

    id = Column("id", Integer, primary_key=True)
    player_name = Column("player_name", VARCHAR(255))
    player_slug = Column("player_slug", VARCHAR(255))
    age = Column("age", Integer, nullable=True)
    position_short_name = Column("position_short_name", VARCHAR(255), nullable=True)
    team_name = Column("team_name", VARCHAR(255), nullable=True)
    team_short_name = Column("team_short_name", VARCHAR(255), nullable=True)
    team_slug = Column("team_slug", VARCHAR(255), nullable=True)
    sci_potential_stars = Column("sci_potential_stars", VARCHAR(255), nullable=True)
    country_code = Column("country_code", VARCHAR(255), nullable=True)
    country_name = Column("country_name", VARCHAR(255), nullable=True)
    estimated_value = Column("estimated_value", VARCHAR(255), nullable=True)
    rank = Column("rank", Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    modified_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


db_engine = connect_db()
