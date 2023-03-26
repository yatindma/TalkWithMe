from pymongo import MongoClient
import configparser


def connect_to_mongodb():
    """
    Connects to MongoDB and returns the chat collection.
    """
    # Read MongoDB configuration from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    connection_string = config.get("MongoDB", "connection_string")
    db_name = config.get("MongoDB", "db_name")
    collection_name = config.get("MongoDB", "collection_name")

    # Connect to MongoDB
    mongo_client = MongoClient(connection_string)
    db = mongo_client[db_name]
    chat_collection = db[collection_name]

    return chat_collection


def store_chat(chat_collection, query, response):
    """
    Stores the chat conversation in the specified MongoDB collection.
    """
    chat = {
        "user_message": query,
        "bot_response": response
    }
    chat_collection.insert_one(chat)
