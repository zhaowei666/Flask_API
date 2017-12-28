from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from base import Base


class Team(Base):
    __tablename__ = 'teams'

    name = Column(String(128), nullable=False, unique=True)


class Draft(Base):
    __tablename__ = 'drafts'

    player_pk = Column(Integer, ForeignKey('players.pk'))
    team_pk = Column(Integer, ForeignKey('teams.pk'))
    season = Column(Integer)
    type = Column(String(128))
    round = Column(Integer)
    pick = Column(Integer)


class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    date_of_birth = Column(Date)


class Game(Base):
    __tablename__ = 'games'

    week = Column(Integer, nullable=False)
    home_team_pk = Column(Integer, ForeignKey('teams.pk'), nullable=False)
    away_team_pk = Column(Integer, ForeignKey('teams.pk'), nullable=False)


class PlayerPerformance(Base):
    __tablename__ = 'player_performances'

    player_pk = Column(Integer, ForeignKey('players.pk'), nullable=False)
    game_pk = Column(Integer, ForeignKey('games.pk'), nullable=False)
    is_home = Column(Boolean)
    yards = Column(Integer)
    completions = Column(Integer)
    interceptions = Column(Integer)
    touchdowns = Column(Integer)
    attempts = Column(Integer)


