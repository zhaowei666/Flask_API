from flask import Blueprint
from views import home


play_bp = Blueprint('player', __name__,
                    url_prefix='',
                    subdomain='player')

play_bp.add_url_rule('/', view_func=home, methods=['GET'])

