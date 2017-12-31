from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from base import Base
from flask import g


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

    @property
    def info(self):
        team = g.session.query(Team).filter_by(pk=self.team_pk).one()
        return "{}: Round {}, Pick {} by {}".format(str(self.season),
                                             str(self.round),
                                             str(self.pick),
                                             team.name
                                             )


class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    date_of_birth = Column(Date)

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)


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


