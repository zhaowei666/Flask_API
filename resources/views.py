from flask import g, render_template, request, jsonify, Response, json
from models import Player, Draft, Game, PlayerPerformance, Team
from webargs.flaskparser import use_args
from webargs import fields
import os
import operator
import numpy as np


def player_info(name):
    first_name = name.split(' ')[0]
    last_name = name.split(' ')[1]
    player = g.session.query(Player).filter_by(
        first_name=first_name,
        last_name=last_name).one()
    draft = g.session.query(Draft).filter_by(player_pk=player.pk).one()
    profile = {'name': player.name,
               'id': player.player_id,
               'date_of_birth': str(player.date_of_birth),
               'draft': draft.info}
    game_logs = []
    performances = g.session.query(PlayerPerformance).filter_by(player_pk=player.pk).all()

    # STATS
    attempts = [p.attempts for p in performances]
    completions = [p.completions for p in performances]
    yards = [p.yards for p in performances]
    touchdowns = [p.touchdowns for p in performances]
    interceptions = [p.interceptions for p in performances]
    stats_all = {'attempts': sum(attempts),
                 'completions': sum(completions),
                 'completion_rate': round(float(sum(completions)) / sum(attempts), 2),
                 'yards': sum(yards),
                 'touchdowns': sum(touchdowns),
                 'interceptions': sum(interceptions)
                 }

    stats_match = {'attempts': round(np.mean(attempts), 2),
                   'completions': round(np.mean(completions), 2),
                   'yards': round(np.mean(yards), 2),
                   'touchdowns': round(np.mean(touchdowns), 2),
                   'interceptions': round(np.mean(interceptions), 2)}

    # Game log
    for performance in performances:
        game = g.session.query(Game).filter_by(pk=performance.game_pk).one()
        home_or_away = 'Home' if performance.is_home else 'Away'
        opponent_pk = game.away_team_pk if performance.is_home else game.home_team_pk
        opponent = g.session.query(Team).filter_by(pk=opponent_pk).one()
        game_logs.append({'week': game.week,
                          'home': home_or_away,
                          'opponent': opponent.name,
                          'yards': performance.yards,
                          'touchdowns': performance.touchdowns,
                          'interceptions': performance.interceptions,
                          'completions': performance.completions,
                          'completion_rate': round(float(performance.completions) / int(performance.attempts), 2),
                          'attempts': performance.attempts
                          })
    game_logs.sort(key=operator.itemgetter('week'))

    return {'profile': profile,
            'stats': {'all': stats_all, 'match': stats_match},
            'gameLogs': game_logs,
            'numLogs': len(game_logs)}


def index():
    players = g.session.query(Player).all()
    names = [x.name for x in players]
    return render_template('player.html',
                           title='Player Profile',
                           names=names,
                           )


def update_player():
    player_name = request.form['name']
    return jsonify(player_info(player_name))


quotes_args = {
    'query': fields.String(required=True)
}

file_address = os.getcwd() + '/data_collection/quotes.json'

with open(file_address, 'r') as f:
    quotes = json.load(f)


@use_args(quotes_args)
def get_quotes(args):
    query = args['query']
    quote_hits = []
    # TODO Spelling isoform finding is required
    for quote in quotes:
        if query in quote['quote']:
            hit = "{} ---- Movie: {} ({})".format(quote['quote'],
                                                  quote['movie_name'],
                                                  quote['movie_year'])
            quote_hits.append(hit)
    return Response(json.dumps(quote_hits), status=200)

