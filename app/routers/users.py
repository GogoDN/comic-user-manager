from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from ..services.users import UsersService
from ..dependencies import AuthHeaders


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


class User(BaseModel):
    id: str
    name: str
    age: int
    token: str


class CreateUserIn(BaseModel):
    name: str
    age: int = Body(0, ge=0)
    password: str


class CreateUserOut(BaseModel):
    inserted_id: str


class LoginIn(BaseModel):
    name: str
    password: str


class LoginOut(BaseModel):
    token: str


@router.post("/", response_model=CreateUserOut)
def create(user: CreateUserIn, service: UsersService = Depends(UsersService)):
    return service.insert_user(user.dict())


@router.post("/login", response_model=LoginOut)
def login(user: LoginIn, service: UsersService = Depends(UsersService)):
    response = service.login(user.name, user.password)
    if not response:
        return JSONResponse({"message": "Invalid credentials"}, 200)
    return response


@router.get("/me", response_model=User)
def me(
    headers: AuthHeaders = Depends(AuthHeaders),
    service: UsersService = Depends(UsersService),
):
    headers.validate_headers()
    return service.me(headers.x_user_id)
