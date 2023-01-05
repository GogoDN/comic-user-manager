from pymongo import MongoClient

from ..config import settings


def run():
    client = MongoClient(settings.mongo_db_conn_str)
    client.comic_store.users.create_index("name", unique=True)
    client.comic_store.users.create_index("token", unique=True)
