from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from functions import *

app = Flask(__name__)

MIN_REPEATED_SIGNS = 25
LOGIN = ''
PASSWORD = ''
ADDRESS = ''
with open('./login.txt', 'r') as file:
    LOGIN = file.read().strip()
with open('./password.txt', 'r') as file:
    PASSWORD = file.read().strip()
with open('./address.txt', 'r') as file:
    ADDRESS = file.read().strip()

MONGO_URI = f'mongodb://{LOGIN}:{PASSWORD}@{ADDRESS}/hashes?authSource=admin'


try:
    client = MongoClient(MONGO_URI)
    db = client.get_database()
    collection = db["hashes"]
    print("Connected to MongoDB")
except ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def default():
    return "Hello I'm working"

@app.route('/write', methods=['POST'])
def write():
    data = request.get_json()
    word = data.get('word', '')
    if not word:
        return jsonify({"msg": "You need to provide a 'word'."}), 400
    hashType = data.get('hashType', '')
    if not hashType or hashType != 'sha256':
        return jsonify({"msg": "You need to provide a 'hashType' (Current support: sha256)."}), 400
    user = data.get('user', '')

    if collection.find_one({"word": word}):
        return jsonify({"msg": "This hash is already in database."}), 400

    hash_in_hex = get_sha256_hash(word)
    hash_in_binary = convert_hex_to_binary(hash_in_hex)
    print(hash_in_binary)
    repeated_counts = count_repeated_pattern_from_start(hash_in_binary)
    if repeated_counts < MIN_REPEATED_SIGNS:
        return jsonify({"msg": f"Your hash has lower that {MIN_REPEATED_SIGNS} repeated signs ({repeated_counts}). "}), 400
    
    write_data = {  "word": word,
                    "isFromBeggining": True,
                    "counts": repeated_counts,
                    "hashType": hashType,
                    "user": user
                    }
    
    try:
        collection.insert_one(write_data)
        return jsonify({"msg": "Hash is successfully added."}), 201
    except Exception as e:
        return jsonify({"msg": "Error inserting data: {e}"}), 500

if __name__ == '__main__':
    HOST = ''
    PORT = ''
    with open('host.txt', 'r') as file:
        adress = file.read().strip()
        HOST = adress.split(':')[0]
        PORT = adress.split(':')[1]
    app.run(host=HOST, port=PORT, debug=False)