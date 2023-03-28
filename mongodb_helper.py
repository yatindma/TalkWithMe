from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
connection_string = config.get("MongoDB", "connection_string")
db_name = config.get("MongoDB", "db_name")
users_collection_name = config.get("MongoDB", "users_collection")
chat_collection_name = config.get("MongoDB", "chat_collection")
sources_collection_name = config.get("MongoDB", "sources_collection")

mongo_client = MongoClient(connection_string)
db = mongo_client[db_name]
users_collection = db[users_collection_name]
chat_collection = db[chat_collection_name]
sources_collection = db[sources_collection_name]


def get_users_collection():
    return users_collection


def get_chat_collection():
    return chat_collection


def get_sources_collection():
    return sources_collection
