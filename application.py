from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import MetaData
from resources import play_bp

default_settings = {
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'DEBUG': False,
    'TESTING': False
}


def base_app():
    '''

    :return: A Flask application
    '''

    app = Flask(__name__)

    ''' Config database and tools'''
    app.config.update(default_settings)
    app.config.from_pyfile('config/config_dev.py')


    # PostgreSQL configuration
    sqlalchemy_settings_key = 'SQLALCHEMY_DATABASE_SETTINGS'
    sqlalchemy_settings = app.config.get(sqlalchemy_settings_key)
    app.config.update({
        'SQLALCHEMY_DATABASE_URI':
            '{protocol}://{user_name}:{password}@{host}:{port}/{db_name}'.format(
                protocol=sqlalchemy_settings.get('PROTOCOL'),
                user_name=sqlalchemy_settings.get('USER_NAME'),
                password=sqlalchemy_settings.get('PASSWORD'),
                host=sqlalchemy_settings.get('HOST'),
                port=sqlalchemy_settings.get('PORT'),
                db_name=sqlalchemy_settings.get('DB_NAME')
            )
    })

    # login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    metadata = MetaData(naming_convention=convention)
    db = SQLAlchemy(app, metadata=metadata)

    @app.before_request
    def before_request():
        g.session = db.session

    return app, db


def create_app():
    app, db = base_app()
    ''' add subdomain '''
    app.register_blueprint(play_bp)

    return app, db
