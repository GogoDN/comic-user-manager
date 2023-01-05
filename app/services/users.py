from fastapi import HTTPException

from bcrypt import hashpw, gensalt, checkpw

from uuid import uuid4

from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from ..data.adapter import MongoDbClient


class UsersService:
    def __init__(self) -> None:
        self.mongo_client = MongoDbClient()

    def __encrypt_password(self, password: str):
        return hashpw(password.encode("utf-8"), gensalt())

    def __find_user_by_id(self, user_id):
        self.validate_user_id(user_id)
        return self.mongo_client.find_user_by_id(user_id)

    def __find_user_by_username(self, username: str):
        return self.mongo_client.find_user_by_name(username)

    def __parse_user_response(self, user: dict):
        return {
            "id": str(user.get("_id")),
            "name": user.get("name"),
            "age": user.get("age"),
            "token": user.get("token"),
        }

    def insert_user(self, user: dict):
        user["password"] = self.__encrypt_password(user["password"])
        user["token"] = str(uuid4())

        try:
            inserted_id = self.mongo_client.insert_user(user)
            return {"inserted_id": str(inserted_id)}
        except DuplicateKeyError as e:
            raise HTTPException(
                422, {"error": {"duplicatedKey": e.details.get("keyValue")}}
            )
        except Exception:
            raise HTTPException(
                503, "A problem occurred while creating the user"
            )

    def login(self, name: str, password: str):
        user = self.__find_user_by_username(name)

        if not user or not checkpw(
            password.encode("utf-8"), user.get("password")
        ):
            return

        return {"token": user.get("token")}

    def me(self, user_id: str):
        user = self.__find_user_by_id(user_id)

        return self.__parse_user_response(user)

    def validate_user_id(self, user_id: str):
        if ObjectId.is_valid(user_id):
            return
        raise HTTPException(422, {"message": "Invalid user id"})
