from flask.ext.script import Manager  
from flask.ext.migrate import Migrate, MigrateCommand  
from app import app, db
from app.settings.models import Settings

manager = Manager(app)  
migrate = Migrate(app, db)  
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
	initial_settings = Settings(currency='euros',
								file_repo='local',
								nb_of_stores=1)
	db.session.add(initial_settings)
	db.session.commit()


if __name__ == "__main__":  
    manager.run()