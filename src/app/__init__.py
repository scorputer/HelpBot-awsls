# app/__init__.py

from flask import Flask
from app.routes import main
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(main)

    # Configure Logging
    setup_logging(app)

    return app

def setup_logging(app):
    log_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    log_file = os.path.join(os.path.dirname(__file__), '..', 'chatbot.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Logging is set up.")
