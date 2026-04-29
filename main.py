import logging
import os
from typing import Annotated

import dotenv
from fastapi import FastAPI, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from database import DB_MANAGER
from logger import get_logger


class User(BaseModel):
    username: str = Field(..., min_length=1, description="Username must be not empty")
    pwd: str = Field(
        ..., min_length=8, description="The password must be at least 8 characters long"
    )


dotenv.load_dotenv("./config/.env")

db_name: str | None = os.getenv("DB_NAME")
db_user: str | None = os.getenv("DB_USER")
db_password: str | None = os.getenv("DB_PASSWORD")
db_host: str | None = os.getenv("DB_HOST")
db_port: str | None = os.getenv("DB_PORT")

app = FastAPI()
logger_server = get_logger("log/server_log.log", name="my_app")


managerDB = DB_MANAGER(db_name, db_user, db_password, db_host, db_port)
managerDB.create_tables()


@app.get("/register/")
async def get_reg_user(user: Annotated[User, Query()]):
    managerDB.create_user(user.username, user.pwd)
    return {"message": user.username}


@app.get("/login/")
async def get_login_user(user: Annotated[User, Query()]):
    managerDB.create_user(user.username, user.pwd)

    return {"message": user.username}


@app.get("/test/")
async def test_endpoint():
    logger_server.info("Test message - should appear once")
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
