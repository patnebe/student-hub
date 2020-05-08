from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from src.config import DevelopmentConfig
from flask_migrate import Migrate

import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

db = SQLAlchemy()

login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    # Setup configurations
    app.config.from_object(config_class)

    # Import blueprints
    from src.app.blueprints.api_v1.controllers import api_v1_bp
    from src.app.blueprints.errors.handlers import errors_bp

    # Register blueprints
    app.register_blueprint(errors_bp)
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    db.init_app(app)

    Migrate(app, db)

    # Setup login manager
    login.init_app(app)

    if not app.debug and not app.testing:
        # enable logging
        if not os.path.exists('logs'):
            os.mkdir('logs')

        APP_NAME = os.environ.get('APP_NAME')
        file_handler = RotatingFileHandler(
            f'logs/{APP_NAME}.log', maxBytes=10240, backupCount=10)

        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(messages)s [in %(pathname)s:%(lineno)d]'))

        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{APP_NAME} startup')

    return app
