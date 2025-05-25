from flask import Blueprint, request

telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.route('/add_telegram_user', methods=['GET'])
def telegram_notification_write():
    """Telegram route [/add_telegram_user]: Represent telegram service"""

    if request.method == 'GET':
        return "In progress...", 200