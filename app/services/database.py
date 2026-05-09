from pymongo import MongoClient
from pymongo.synchronous.collection import Collection 

from app.utils.notification import log

class Database:
    def __init__(self, name: str = None, login: str = None, ip_and_port: str = None) -> None:

        self.__name: str = name
        self.__login: str = login
        self.__ip_and_port: str = ip_and_port
        
        self.__client: MongoClient = MongoClient()
        self.__database = None

        self.__is_connected: bool = False

    def init(self, name: str, login: str, ip_and_port: str) -> None:
        self.__name = name
        self.__login = login
        self.__ip_and_port = ip_and_port

    def set_login(self, login: str) -> None:
        self.__login = login

    def is_connected(self) -> bool:
        return self.__is_connected
    
    def set_ip_and_port(self, ip_and_port: str) -> None:
        ip, port = ip_and_port.split(':')
        port = int(port)
        self.__ip_and_port = f"{ip}:{port}"
    
    def connect(self, password: str) -> None:
        if self.__login and self.__name and self.__ip_and_port:
            MONGO_URI = f'mongodb://{self.__login}:{password}@{self.__ip_and_port}/{self.__name}?authSource=admin'
        else:
            raise ValueError("Not enought data to initialize database.")
        try:
            self.__client = MongoClient(MONGO_URI)
            self.__database = self.__client.get_database()
            self.__is_connected = True
            log("Database", "Connected to MongoDB")
        except ConnectionError as e:
            self.__is_connected = False
            log("Database", f"Error connecting to MongoDB: {e}")

    def __check_connection(self, collection: str) -> None:
        if not self.is_connected:
            raise ConnectionError("Database: Not connected to the database.")

    def find(self, collection: str, query: dict, sort: list = None, skip: int = 0, limit: int = 0) -> list:
        self.__check_connection(collection)

        if collection is None:
            raise ValueError("Database: Active collection is not set.")


        cursor = self.__database[collection].find(query)
        if sort:
            cursor.sort(sort)
        cursor.skip(skip)
        if limit > 0:
            cursor.limit(limit)

        return list(cursor)
    
    def find_one(self, collection: str, query: dict):
        self.__check_connection(collection)
        return self.__database[collection].find_one(query)
    
    def insert_one(self, collection: str, query: dict):
        self.__check_connection(collection)
        self.__database[collection].insert_one(query)
    
    def count(self, collection: str, query: dict = {}) -> int:
        self.__check_connection(collection)
        return self.__database[collection].count_documents(query)

    def delete_one(self, collection: str, filter: dict = {}):
        self.__check_connection(collection)
        self.__database[collection].delete_one(filter)

    def delete(self, collection: str, filter: dict = {}):
        self.__check_connection(collection)
        self.__database[collection].delete_many(filter)