import os
import socket
from datetime import datetime
import ssl

from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

from functions import *

load_dotenv()
app = Flask(__name__)

app.config['DATABASE_IP_AND_PORT'] = os.getenv('DATABASE_IP_AND_PORT')
app.config['TELEGRAM_BOT_IP_AND_PORT'] = os.getenv('TELEGRAM_BOT_IP_AND_PORT')
app.config['DATABASE_LOGIN'] = os.getenv('DATABASE_LOGIN')
app.config['DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['HOST'] = os.getenv('HOST')
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
app.config['PEM_PASS'] = os.getenv('PEM_PASS')

MIN_REPEATED_SIGNS: int = 25
MAX_USER_LENGTH: int = 31
MAX_WORD_LENGTH: int = 255
ROW_IN_ONE_PAGE_LIMIT: int = 100

TELEGRAM_IP, TELEGRAM_PORT = app.config['TELEGRAM_BOT_IP_AND_PORT'].split(':')

MONGO_URI = f'mongodb://{app.config['DATABASE_LOGIN']}\
:{app.config['DATABASE_PASSWORD']}@{app.config['DATABASE_IP_AND_PORT']}\
/hashes?authSource=admin'

# Connect to mongodb
try:
    client = MongoClient(MONGO_URI)
    db = client.get_database()
    collection = db["hashes"]
    print("Connected to MongoDB")
except ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/view')
def view():
    return redirect(url_for('view_with_params', page=1, created_at=-1))

@app.route('/view/<int:page>')
def view_with_params(page: int):
    sort_data = []
    sort_args = ['word, isFromBeggining', 'counts', 'hashType', 'user', 'created_at']
    for arg in sort_args:
        temp = request.args.get(arg, '0')
        if temp == '1':
            sort_data.append((arg, 1))
        elif temp == '-1':
            sort_data.append((arg, -1))
    if sort_data:
        result = list(collection.find().sort(sort_data).skip(ROW_IN_ONE_PAGE_LIMIT*(page-1)).limit(ROW_IN_ONE_PAGE_LIMIT))
    else:
        result = list(collection.find().skip(ROW_IN_ONE_PAGE_LIMIT*(page-1)).limit(ROW_IN_ONE_PAGE_LIMIT))
    count = collection.count_documents({})

    return render_template('view.html', result=result, count=count, page=count//ROW_IN_ONE_PAGE_LIMIT+1)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')
    
    data = request.get_json()
    word: str = data.get('word', '')
    hashType: str = data.get('hashType', '')
    user: str = data.get('user', '')

    # Validation (1/2) Process before finding a hash
    if not word:
        return jsonify({"msg": "You need to provide a 'word'."}), 400
    if len(word) > MAX_WORD_LENGTH:
        return jsonify({"msg": f"You reach the max length of the word. Max length is {MAX_WORD_LENGTH} (Your: {len(word)})."}), 400
    if len(user) > MAX_USER_LENGTH:
        return jsonify({"msg": f"You reach the max length of the user. Max length is {MAX_USER_LENGTH} (Your: {len(user)})."}), 400
    if not hashType or hashType != 'sha256':
        return jsonify({"msg": "You need to provide a 'hashType' (Current support: sha256)."}), 400
    if collection.find_one({"word": word}):
        return jsonify({
            "errno": 1,
            "msg": "This hash is already in database."
        }), 400

    # Find hash
    hash_in_hex = get_sha256_hash(word)
    hash_in_binary = convert_hex_to_binary(hash_in_hex)
    repeated_counts = count_repeated_pattern_from_start(hash_in_binary)

    # Validation (2/2) Checking if hash actual a rare one
    if repeated_counts < MIN_REPEATED_SIGNS:
        return jsonify({
            "errno": 2,
            "msg": f"Your hash has lower that {MIN_REPEATED_SIGNS} repeated signs ({repeated_counts}). "
        }), 400
    
    created_at = datetime.utcnow()

    # Send to a telegram bot
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((TELEGRAM_IP, int(TELEGRAM_PORT)))
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
        collection.insert_one(write_data)
        return jsonify({
            "errno": 0,
            "msg": "Hash is successfully added."
        }), 201
    except Exception as e:
        return jsonify({
            "errno": 3,
            "msg": "Database is currently unavailable. Please try again later."}), 500
    
    

if __name__ == '__main__':
    IP, PORT = os.getenv('HOST').split(':')
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('./ssl/rareHashes.crt', './ssl/rareHashes.key', password=app.config['PEM_PASS'])
    app.run(host=IP,
            port=int(PORT),
            debug=app.config['DEBUG'],
            ssl_context=ssl_context)