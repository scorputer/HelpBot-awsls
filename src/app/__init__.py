# app/__init__.py

from flask import Flask
from app.routes import main
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug  # Enable or disable debug mode

    # Register Blueprints
    app.register_blueprint(main)

    # Configure Logging
    setup_logging(app, debug)

    return app

def setup_logging(app, debug):
    # Set log level based on debug mode
    log_level = logging.DEBUG if debug else logging.INFO

    # Create log formatter
    log_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )

    # Create log directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # File handler for logging
    log_file = os.path.join(log_dir, 'chatbot.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(log_level)

    # Clear existing handlers to avoid duplication
    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(log_level)

    app.logger.info("Logging is set up.")
    app.logger.debug("Debug mode is enabled.")
