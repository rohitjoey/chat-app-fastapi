from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from . import schemas, services

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/create", status_code=201, response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(
        user,
        db,
    )


@auth_router.post("/login", status_code=200, response_model=schemas.UserWithToken)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    return await services.login_user(
        schemas.UserAuth(email=form_data.username, password=form_data.password),
        db,
    )


@auth_router.get("/me", response_model=schemas.User)
async def get_me(current_user: schemas.User = Depends(services.get_current_user)):
    return current_user
