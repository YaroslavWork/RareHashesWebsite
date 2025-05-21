from flask import request, render_template, jsonify, Blueprint, current_app
from datetime import datetime
import socket

from app.utils.hash_utils import get_sha256_hash, convert_hex_to_binary, count_repeated_pattern_from_start

write_bp = Blueprint("write", __name__)

@write_bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')
    
    max_word_length = current_app.config['MAX_WORD_LENGTH']
    max_user_length = current_app.config['MAX_USER_LENGTH']
    min_repeated_signs = current_app.config['MIN_REPEATED_SIGNS']
    database = current_app.config['DATABASE']
    telegram_ip, telegram_port = current_app.config['TELEGRAM_BOT_IP_AND_PORT'].split(':')

    data = request.get_json()
    word: str = data.get('word', '')
    hashType: str = data.get('hashType', '')
    user: str = data.get('user', '')

    # Validation (1/2) Process before finding a hash
    if not word:
        return jsonify({"msg": "You need to provide a 'word'."}), 400
    if len(word) > max_word_length:
        return jsonify({"msg": f"You reach the max length of the word. Max length is {max_word_length} (Your: {len(word)})."}), 400
    if len(user) > max_user_length:
        return jsonify({"msg": f"You reach the max length of the user. Max length is {max_word_length} (Your: {len(user)})."}), 400
    if not hashType or hashType != 'sha256':
        return jsonify({"msg": "You need to provide a 'hashType' (Current support: sha256)."}), 400
    if database.find_one(query={"word": word}):
        return jsonify({
            "errno": 1,
            "msg": "This hash is already in database."
        }), 400

    # Find hash
    hash_in_hex = get_sha256_hash(word)
    hash_in_binary = convert_hex_to_binary(hash_in_hex)
    repeated_counts = count_repeated_pattern_from_start(hash_in_binary)

    # Validation (2/2) Checking if hash actual a rare one
    if repeated_counts < min_repeated_signs:
        return jsonify({
            "errno": 2,
            "msg": f"Your hash has lower that {min_repeated_signs} repeated signs ({repeated_counts}). "
        }), 400
    
    created_at = datetime.utcnow()

    # Send to a telegram bot
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((telegram_ip, int(telegram_port)))
        client.sendall(f"{word}|NEXT|{True}|NEXT|{hashType}|NEXT|{repeated_counts}|NEXT|{user}|NEXT|{created_at}\n".encode('utf-8'))
        client.close()
    except ConnectionRefusedError as e:
        
        print(f"Connection Refused: {e}")

    # Writing to a database
    write_data = {  "word": word,
                    "isFromBeggining": True,
                    "counts": repeated_counts,
                    "hashType": hashType,
                    "user": user,
                    "created_at": created_at
                    }
    
    try:
        database.insert_one(query=write_data)
        return jsonify({
            "errno": 0,
            "msg": "Hash is successfully added."
        }), 201
    except Exception as e:
        return jsonify({
            "errno": 3,
            "msg": "Database is currently unavailable. Please try again later."}), 500
   