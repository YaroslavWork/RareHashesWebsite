from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

LOGIN = ''
PASSWORD = ''
ADDRESS = ''
with open('./login.txt', 'r') as file:
    LOGIN = file.read.strip()
with open('./password.txt', 'r') as file:
    PASSWORD = file.read.strip()
with open('./address.txt', 'r') as file:
    ADDRESS = file.read.strip()

MONGO_URI = f'mongodb://{LOGIN}:{PASSWORD}@{ADDRESS}/hashes'