from app.services.database import Database
from app.models.hash import Hash

def add_hash_to_database(database: Database, hash: Hash):
    write_data = hash.to_dict()
    database.set_active_collection('hashes')
    database.insert_one(query=write_data)