from models import Player, Team, PlayerPerformance, Draft, Game
from application import create_app
import pandas as pd

player_csv_url = 'https://s3.amazonaws.com/web.profootballfocus.com/players.csv'
stats_csv_url = 'https://s3.amazonaws.com/web.profootballfocus.com/statistics.csv'


#try:
#    db = psycopg2.connect("dbname='player_db' user='dev_user' password='dev_password' port='5430'")
#except:
#    raise NotImplementedError("Not able to connect to postgreSQL database.")

app, db = create_app()

player_table = pd.read_csv(player_csv_url)
stats_table = pd.read_csv(stats_csv_url)


def add_players():
    for idx, row in player_table.iterrows():
        player = Player()
        player.player_id = row['player_id']
        player.last_name = row['last_name']
        player.first_name = row['first_name']
        player.date_of_birth = row['date_of_birth']
        db.session.add(player)
        db.session.commit()


def add_teams():
    team_names = set(stats_table['home_team']) | set(stats_table['away_team'])
    for team_name in team_names:
        team = Team()
        team.name = team_name
        db.session.add(team)
        db.session.commit()





def add_draft():
    for idx, row in player_table.iterrows():
        draft = Draft()
        player = db.session.query(Player).filter_by(player_id=row['player_id']).one()
        team = db.session.query(Team).filter_by(name=row['drafted_by']).one()
        draft.player_pk = player.pk
        draft.team_pk = team.pk
        draft.season = row['draft_season']
        draft.type = row['draft_type']
        draft.round = row['draft_round']
        draft.pick = row['draft_pick']
        db.session.add(draft)
        db.session.commit()



def add_games():
    for idx, row in stats_table.iterrows():
        game = Game()
        game.week = row['week']
        home_team = db.session.query(Team).filter_by(name=row['home_team']).one()
        game.home_team_pk = home_team.pk
        away_team = db.session.query(Team).filter_by(name=row['away_team']).one()
        game.away_team_pk = away_team.pk
        if not db.session.query(Game).filter_by(week=row['week'],
                                                home_team_pk=home_team.pk,
                                                away_team_pk=away_team.pk).one_or_none():
            db.session.add(game)
            db.session.commit()


def add_player_performance():
    for idx, row in stats_table.iterrows():
        player_performance = PlayerPerformance()
        player = db.session.query(Player).filter_by(player_id=row['player_id']).one()
        player_performance.player_pk = player.pk
        home_team = db.session.query(Team).filter_by(name=row['home_team']).one()
        away_team = db.session.query(Team).filter_by(name=row['away_team']).one()
        game = db.session.query(Game).filter_by(week=row['week'],
                                                home_team_pk=home_team.pk,
                                                away_team_pk=away_team.pk).one()
        player_performance.game_pk = game.pk
        player_performance.is_home = row['on_home_team']
        player_performance.yards = row['yards']
        player_performance.completions = row['completions']
        player_performance.interceptions = row['interceptions']
        player_performance.touchdowns = row['touchdowns']
        player_performance.attempts = row['attempts']
        db.session.add(player_performance)
        db.session.commit()


if __name__ == '__main__':
    add_players()
    add_teams()
    add_games()
    add_draft()
    add_player_performance()


