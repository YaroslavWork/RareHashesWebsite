from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from functions import *
from datetime import datetime

app = Flask(__name__)

MIN_REPEATED_SIGNS: int = 25
MAX_USER_LENGTH: int = 31
MAX_WORD_LENGTH: int = 255
ROW_IN_ONE_PAGE_LIMIT: int = 100
LOGIN: str = ''
PASSWORD: str = ''
ADDRESS: str = ''

with open('./login.txt', 'r') as file:
    LOGIN = file.read().strip()
with open('./password.txt', 'r') as file:
    PASSWORD = file.read().strip()
with open('./address.txt', 'r') as file:
    ADDRESS = file.read().strip()

MONGO_URI = f'mongodb://{LOGIN}:{PASSWORD}@{ADDRESS}/hashes?authSource=admin'

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
        return jsonify({"msg": "This hash is already in database."}), 400

    # Find hash
    hash_in_hex = get_sha256_hash(word)
    hash_in_binary = convert_hex_to_binary(hash_in_hex)
    repeated_counts = count_repeated_pattern_from_start(hash_in_binary)

    # Validation (2/2) Checking if hash actual a rare one
    if repeated_counts < MIN_REPEATED_SIGNS:
        return jsonify({"msg": f"Your hash has lower that {MIN_REPEATED_SIGNS} repeated signs ({repeated_counts}). "}), 400
    
    # Writing to a database
    write_data = {  "word": word,
                    "isFromBeggining": True,
                    "counts": repeated_counts,
                    "hashType": hashType,
                    "user": user,
                    "created_at": datetime.utcnow()
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
    app.run(host=HOST, port=PORT, debug=True)