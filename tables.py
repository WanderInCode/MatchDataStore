from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, NVARCHAR, DATETIME, INTEGER, BOOLEAN

Base = declarative_base()


class Team(Base):

    __tablename__ = 'team'

    league_id = Column(BIGINT, primary_key=True)
    team_id = Column(BIGINT, primary_key=True)
    team_tag = Column(NVARCHAR(10))
    team_name = Column(NVARCHAR(25))


class Player(Base):

    __tablename__ = 'player'

    league_id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, primary_key=True)
    team_id = Column(BIGINT, nullable=False)
    player_name = Column(NVARCHAR(25))


class Match(Base):

    __tablename__ = 'match'

    match_id = Column(BIGINT, primary_key=True)
    league_id = Column(BIGINT, nullable=False)
    start_time = Column(DATETIME, nullable=False)
    duration = Column(INTEGER, nullable=False)
    radiant_win = Column(BOOLEAN, nullable=False)
    radiant_team_id = Column(BIGINT, nullable=False)
    dire_team_id = Column(BIGINT, nullable=False)
    radiant_score = Column(INTEGER, nullable=False)
    dire_score = Column(INTEGER, nullable=False)


class MatchDetail(Base):

    __tablename__ = 'match_detail'
