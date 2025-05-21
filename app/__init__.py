from flask import Flask
from dotenv import load_dotenv
import os

from app.services.database import Database


def create_app():
    app = Flask(__name__)

    # --- Load .env ---
    load_dotenv()
    app.config['DATABASE_IP_AND_PORT'] = os.getenv('DATABASE_IP_AND_PORT')
    app.config['TELEGRAM_BOT_IP_AND_PORT'] = os.getenv('TELEGRAM_BOT_IP_AND_PORT')
    app.config['DATABASE_LOGIN'] = os.getenv('DATABASE_LOGIN')
    app.config['DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
    app.config['HOST'] = os.getenv('HOST')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
    app.config['PEM_PASS'] = os.getenv('PEM_PASS')

    # --- Constants ---
    app.config['MIN_REPEATED_SIGNS'] = 25
    app.config['MAX_USER_LENGTH'] = 31
    app.config['MAX_WORD_LENGTH'] = 255
    app.config['ROW_IN_ONE_PAGE_LIMIT'] = 100  # For users (in view routes)

    # --- Database configuration ---
    database = Database(
        login=app.config['DATABASE_LOGIN'],
        ip_and_port=app.config['DATABASE_IP_AND_PORT']
    )   

    database.connect(password=app.config['DATABASE_PASSWORD'])
    database.set_active_collection('hashes')
    app.config['DATABASE'] = database

    # --- Register blueprints ---
    from app.routes.main_routes import main_bp
    from app.routes.telegram_routes import telegram_bp
    from app.routes.write_routes import write_bp
    from app.routes.view_routes import view_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(telegram_bp)
    app.register_blueprint(write_bp)
    app.register_blueprint(view_bp)

    return app