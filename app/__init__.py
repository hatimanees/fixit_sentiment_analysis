from flask import Flask
from flask_cors import CORS
from app.config import Config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS with the app
    CORS(app)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app