from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .api import users, groups, questions, progress
    app.register_blueprint(users.bp)
    app.register_blueprint(groups.bp)
    app.register_blueprint(questions.bp)
    app.register_blueprint(progress.bp)

    return app