from flask import Blueprint
from views import player_selection, update_player


play_bp = Blueprint('player', __name__,
                    url_prefix='',
                    subdomain='player')

play_bp.add_url_rule('/', view_func=player_selection, methods=['GET'])
play_bp.add_url_rule('/update_player', view_func=update_player, methods=['POST'])
