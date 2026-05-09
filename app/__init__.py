from flask import Flask
from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv
import time
import os
import asyncio
import threading

from app.extensions import login_manager, database, telegram_api
from app.models.user import User
from app.utils.notification import log


def start_telegramAPI_loop(telegramAPI, password):
    while True:
        if not telegramAPI.is_open():
            log("RabbitMQ", "Connect to server...")
            asyncio.run(telegramAPI.open_connection(password))
        time.sleep(30)
        

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    return User.from_dict(user_data) if user_data else None


def create_app():
    # --- Load .env ---
    load_dotenv()


    # --- Init app ---
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', '')
    if app.secret_key == '':
        raise ValueError('Provide secret key in .env file.')


    # --- Load constants ---
    app.config['DATABASE_IP_AND_PORT'] = os.getenv('DATABASE_IP_AND_PORT')
    app.config['DATABASE_NAME'] = os.getenv('DATABASE_NAME')
    app.config['DATABASE_LOGIN'] = os.getenv('DATABASE_LOGIN')
    app.config['DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
    app.config['HOST'] = os.getenv('HOST')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
    app.config['PEM_PASS'] = os.getenv('PEM_PASS')
    app.config['RABBIT_LOGIN'] = os.getenv('RABBIT_LOGIN')
    app.config['RABBIT_PASSWORD'] = os.getenv('RABBIT_PASSWORD')
    app.config['RABBIT_HOST'] = os.getenv('RABBIT_HOST')


    # --- Constants ---
    app.config['MIN_REPEATED_SIGNS'] = 25
    app.config['MAX_USER_LENGTH'] = 31
    app.config['MAX_TELEGRAMID_LENGTH'] = 32
    app.config['MAX_WORD_LENGTH'] = 255
    app.config['ROW_IN_ONE_PAGE_LIMIT'] = 100  # For users (in view routes)


    # --- Database configuration ---
    database.init(
        name=app.config['DATABASE_NAME'],
        login=app.config['DATABASE_LOGIN'],
        ip_and_port=app.config['DATABASE_IP_AND_PORT']
    )   
    database.connect(password=app.config['DATABASE_PASSWORD'])


    # --- Login configuration ---
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'


    # --- TelegramAPI configuration ---
    telegram_api.init(rabbit_login=app.config['RABBIT_LOGIN'], rabbit_host=app.config['RABBIT_HOST'])
    telegram_api_thread = threading.Thread(target=start_telegramAPI_loop, args=(telegram_api, app.config['RABBIT_PASSWORD']))
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        telegram_api_thread.start()


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