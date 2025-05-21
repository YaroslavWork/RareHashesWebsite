from flask import Blueprint, request

telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.route('/add_telegram_user', methods=['GET', 'POST'])
def telegram_notification_write():
    if request.method == 'GET':
        return "In progress..."