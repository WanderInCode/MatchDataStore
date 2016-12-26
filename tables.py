from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, NVARCHAR, DATETIME, INTEGER, BOOLEAN, TINYINT, FLOAT

Base = declarative_base()


class Team(Base):

    __tablename__ = 'team'

    league_id = Column(BIGINT, primary_key=True)
    team_id = Column(BIGINT, primary_key=True)
    team_tag = Column(NVARCHAR(10))
    team_name = Column(NVARCHAR(25))

    def __init__(self, item):
        for name, value in item.items():
            setattr(self, name, value)


class Player(Base):

    __tablename__ = 'player'

    league_id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, primary_key=True)
    team_id = Column(BIGINT, nullable=False)
    player_name = Column(NVARCHAR(25))

    def __init__(self, item):
        for name, value in item.items():
            setattr(self, name, value)


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
    cluster = Column(INTEGER, nullable=False)

    def __init__(self, item):
        for name, value in item.items():
            setattr(self, name, value)


class MatchDetail(Base):

    __tablename__ = 'match_detail'

    match_id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, primary_key=True)
    player_slot = Column(TINYINT, nullable=False)
    hero_id = Column(INTEGER, nullable=False)
    kills = Column(INTEGER, nullable=False)
    deaths = Column(INTEGER, nullable=False)
    assists = Column(INTEGER, nullable=False)
    last_hits = Column(INTEGER, nullable=False)
    denies = Column(INTEGER, nullable=False)
    gold_per_min = Column(FLOAT, nullable=False)
    xp_per_min = Column(FLOAT, nullable=False)
    level = Column(TINYINT, nullable=False)
    hero_damage = Column(INTEGER, nullable=False)
    tower_damage = Column(INTEGER, nullable=False)
    hero_healing = Column(INTEGER, nullable=False)
    gold = Column(INTEGER, nullable=False)
    gold_spent = Column(INTEGER, nullable=False)

    def __init__(self, item):
        for name, value in item.items():
            setattr(self, name, value)
