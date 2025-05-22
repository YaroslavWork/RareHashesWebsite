from flask import request, render_template, jsonify, Blueprint, current_app
from datetime import datetime
import asyncio

from app.utils.hash_utils import get_sha256_hash, convert_hex_to_binary, count_repeated_pattern_from_start
from app.database_utils.hash_database_utils import add_hash_to_database
from app.models.hash import Hash

write_bp = Blueprint("write", __name__)

@write_bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')
    
    max_word_length = current_app.config['MAX_WORD_LENGTH']
    max_user_length = current_app.config['MAX_USER_LENGTH']
    min_repeated_signs = current_app.config['MIN_REPEATED_SIGNS']
    database = current_app.config['DATABASE']
    telegramAPI = current_app.config['TELEGRAMAPI']

    hash = Hash()

    data = request.get_json()
    hash.word = data.get('word', None)
    hash.isFromBeginning = True
    hash.hashType = data.get('hashType', None)
    hash.user = data.get('user', None)

    # Validation (1/2) Process before finding a hash
    if hash.word is None:
        return jsonify({"msg": "You need to provide a 'word'."}), 400
    if len(hash.word) > max_word_length:
        return jsonify({"msg": f"You reach the max length of the word. Max length is {max_word_length} (Your: {len(hash.word)})."}), 400
    if len(hash.user) > max_user_length:
        return jsonify({"msg": f"You reach the max length of the user. Max length is {max_word_length} (Your: {len(hash.ser)})."}), 400
    if hash.hashType is None or hash.hashType != 'sha256':
        return jsonify({"msg": "You need to provide a 'hashType' (Current support: sha256)."}), 400
    if database.find_one(query={"word": hash.word}):
        return jsonify({
            "errno": 1,
            "msg": "This hash is already in database."
        }), 400

    # Find hash
    hash_in_hex = get_sha256_hash(hash.word)
    hash_in_binary = convert_hex_to_binary(hash_in_hex)
    hash.counts = count_repeated_pattern_from_start(hash_in_binary)

    # Validation (2/2) Checking if hash actual a rare one
    if hash.counts < min_repeated_signs:
        return jsonify({
            "errno": 2,
            "msg": f"Your hash has lower that {min_repeated_signs} repeated signs ({hash.counts}). "
        }), 400
    
    hash.createdAt = datetime.utcnow()

    print(hash)
    if not hash.is_complete():
        return jsonify({
            "errno": 3,
            "msg": "Something wrong with the code. Try later..."}), 400

    # Send to a telegram bot
    telegramAPI.notify(hash, 100)

    try:
        add_hash_to_database(database=database, hash=hash)
        return jsonify({
            "errno": 0,
            "msg": "Hash is successfully added."
        }), 201
    except Exception as e:
        return jsonify({
            "errno": 3,
            "msg": "Database is currently unavailable. Please try again later."}), 500
   