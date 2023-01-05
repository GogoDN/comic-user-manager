from fastapi import FastAPI

from .routers import users

from .scripts import db_bootsrap

db_bootsrap.run()

app = FastAPI()

app.include_router(users.router)
