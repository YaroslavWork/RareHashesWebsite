from pymongo import MongoClient
from pymongo.synchronous.collection import Collection 

class Database:
    DATABASE_NAME = 'hashes'
    COLLECTION_NAME = 'hashes'

    def __init__(self, login: str, ip_and_port: str) -> None:

        self.__login: str = login
        self.__ip_and_port: str = ip_and_port
        
        self.__client: MongoClient = MongoClient()
        self.__database = None
        self.__active_collection = None

        self.__is_connected: bool = False

    def set_login(self, login: str) -> None:
        self.__login = login

    def is_connected(self) -> bool:
        return self.__is_connected
    
    def set_ip_and_port(self, ip_and_port: str) -> None:
        ip, port = ip_and_port.split(':')
        port = int(port)
        self.__ip_and_port = f"{ip}:{port}"

    def set_active_collection(self, collection_name: str) -> None:
        self.__active_collection = self.__database[collection_name]
    
    def connect(self, password: str) -> None:
        MONGO_URI = f'mongodb://{self.__login}:{password}@{self.__ip_and_port}/{Database.DATABASE_NAME}?authSource=admin'
        
        try:
            self.__client = MongoClient(MONGO_URI)
            self.__database = self.__client.get_database()
            self.__is_connected = True
            print("Database: Connected to MongoDB")
        except ConnectionError as e:
            self.__is_connected = False
            print(f"Databas: Error connecting to MongoDB: {e}")

    def find(self, query: dict, sort: list = None, skip: int = 0, limit: int = 0) -> list:
        if not self.is_connected:
            raise ConnectionError("Database: Not connected to the database.")
        if self.__active_collection is None:
            raise ValueError("Database: Active collection is not set.")
        
        cursor = self.__active_collection.find(query)
        if sort:
            cursor.sort(sort)
        cursor.skip(skip)
        if limit > 0:
            cursor.limit(limit)

        return list(cursor)
    
    def find_one(self, query: dict):
        return self.__active_collection.find_one(query)
    
    def insert_one(self, query: dict):
        self.__active_collection.insert_one(query)
    
    def count(self, query: dict = {}) -> int:
        return self.__active_collection.count_documents(query)

