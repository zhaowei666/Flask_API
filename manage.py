from gevent import monkey
monkey.patch_all()
from flask_script import Manager, Command, Option
from flask_migrate import Migrate, MigrateCommand
from application import create_app
from models import Base


class RunApplication(Command):
    option_list = (
        Option('-o', '--open-host', action='store_true', dest='open_host', default=False),
    )

    def __init__(self, app):
        super(RunApplication, self).__init__()
        self.app = app

    def run(self, open_host):
        host = 'localhost'
        port = 5000

        self.app.run(host=host,
                     port=port,
                     debug=True,
                     threaded=True)


def main():

    app, db = create_app()
    migrate = Migrate(app, Base)

    # Flask-Script manager
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.add_command('run', RunApplication(app))
    manager.run()

if __name__ == '__main__':
    main()
