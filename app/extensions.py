from flask_login import LoginManager

from app.services.database import Database
from app.services.telegram_api import TelegramAPI


# --- Flask Login Manager ---
login_manager = LoginManager()

# --- MongoDB Database ---
database = Database()

# --- Telegram API Bot ---
telegram_api = TelegramAPI()