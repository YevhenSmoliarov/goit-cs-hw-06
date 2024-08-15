from pymongo import MongoClient

def save_to_mongodb(data):
    client = MongoClient("mongodb://mongo:27017/")
    db = client['chat_database']
    messages = db['messages']
    messages.insert_one(data)
