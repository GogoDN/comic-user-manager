from pymongo import MongoClient
from bson import ObjectId

from ..config import settings


class MongoDbClient:
    def __init__(self) -> None:
        self.client = MongoClient(settings.mongo_db_conn_str)

    def __get_comic_store_db(self):
        return self.client.comic_store

    def __get_users_collection(self):
        db = self.__get_comic_store_db()
        return db.users

    def find_user_by_id(self, user_id):
        collection = self.__get_users_collection()
        return collection.find_one({"_id": ObjectId(user_id)})

    def find_user_by_name(self, name):
        collection = self.__get_users_collection()
        return collection.find_one({"name": name})

    def insert_user(self, user):
        collection = self.__get_users_collection()
        new_user = collection.insert_one(user)
        return new_user.inserted_id
