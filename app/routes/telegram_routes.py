import threading
import queue
from flask import Blueprint, jsonify, render_template, request, current_app

from app.telegram_utils.notification_service_utils import add_new_user, wait_until_response

telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.route('/telegram_notification_service', methods=['GET', 'POST'])
async def telegram_notification_service():
    """Telegram route [/telegram_notification_service]: Represent telegram service"""

    if request.method == 'GET':
        return render_template('telegramNotificationService.html'), 200
    
    max_telegramID_length = current_app.config['MAX_TELEGRAMID_LENGTH']
    telegramAPI = current_app.config['TELEGRAMAPI']

    data = request.get_json()

    telegram_operation = data.get("telegram_operation", None)
    telegramID = data.get("telegram_id", None)
    rule_type = data.get("rule_type", None)
    minimum_value = data.get("minimum_value", None)
    
    # Validation
    if telegram_operation is None:
        return jsonify({"msg": "You need to provide a 'telegram_operation'."}), 400
    if telegram_operation not in ['add', 'remove']:
        return jsonify({"msg": "'telegram_operation' only support 'add' and 'remove' command."}), 400
    if telegramID is None:
        return jsonify({"msg": "You need to provide a 'telegram_id'."}), 400
    if not telegramID.isdigit():
        return jsonify({"msg": "'telegram_id' must be a number."}), 400
    if len(telegramID) > max_telegramID_length:
        return jsonify({"msg": f"You reach the max length of the user. Max length is {max_telegramID_length} (Your: {len(telegramID)})."}), 400
    if rule_type is None:
        return jsonify({"msg": "You need to provide a 'rule_type'."}), 400
    if rule_type not in ['rarity', 'ranking']:
        return jsonify({"msg": "'rule_type' only support 'rarity' and 'ranking' command."}), 400
    if not minimum_value.isdigit():
        return jsonify({"msg": "'minimum_value' must be a number."}), 400
    if not (0 < int(minimum_value) <= 100_000_000):
        return jsonify({"msg": "'minimum_value' must be in a range between 1 and 100 000 000."}), 400
    
    if telegram_operation == 'add':
        message_uuid: str = add_new_user(telegramAPI, telegramID, rule_type, minimum_value)
        value = await wait_until_response(telegramAPI, message_uuid, max_time_in_seconds=5)
        if value == 0:
            return jsonify({
                "errno": 0,
                "msg": "Telegram user is successfully register."
            }), 201
        elif value == 1 or value == 2:
            return jsonify({
                "errno": 1,
                "msg": "Something went wrong. Try again later."
            }), 400
        elif value == -1:
            return jsonify({
                "errno": 2,
                "msg": "Telegram bot is currently unavailable. Try again later."
            }), 503
        elif value == 3:
            return jsonify({
                "errno": 3,
                "msg": "This user is already in notification service."
            }), 400
    else:
        return jsonify({
            "msg": "Not Implemented..."
        }), 501