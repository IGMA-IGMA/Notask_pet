from typing import Annotated, Literal

from fastapi import FastAPI, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from database import DB_MANAGER


class User(BaseModel):
    username: str = Field(..., min_length=1, description="Username must be not empty")
    pwd: str = Field(..., min_length=8,
                     description="The password must be at least 8 characters long")


app = FastAPI()
managerDB = DB_MANAGER("pet", "pet", "pet", "localhost", "5432")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/reg_user/")
async def get_reg_user(user: Annotated[User, Query()]):
    managerDB.create_user(user.username, user.pwd)

    return {"message": user.username}

@app.get("/login/")
async def get_login_user(user: Annotated[User, Query()]):
    managerDB.create_user(user.username, user.pwd)

    return {"message": user.username}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
