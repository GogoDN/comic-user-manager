from fastapi import Header, HTTPException

from typing import Union

from .data.adapter import MongoDbClient


class AuthHeaders:
    def __init__(
        self,
        x_user_id: Union[str, None] = Header(None),
        x_token: Union[str, None] = Header(None),
    ) -> None:
        self.x_user_id = x_user_id
        self.x_token = x_token

    def validate_headers(self):
        if not self.x_user_id or not self.x_token:
            raise HTTPException(401)

        if self.x_user_id:
            user = MongoDbClient().find_user_by_id(self.x_user_id)
            if user.get("token") != self.x_token:
                raise HTTPException(401)
