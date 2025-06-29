from datetime import timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db

from ..config import JWT_EXPIRES
from . import models, schemas, utils
from .dependencies import oauth2_scheme


def create_user(
    user: schemas.UserCreate,
    db: Session,
):
    user_data = user.model_dump()
    if get_user_by_email(user_data["email"], db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same email already exists",
        )
    user_data["hashed_password"] = utils.get_password_hash(user.password)
    del user_data["password"]
    db_item = models.User(**user_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def login_user(user: schemas.UserAuth, db: Session):
    user_from_DB = get_user_by_email(user.email, db)
    if not user_from_DB:
        raise HTTPException(
            status_code=404,
            detail="Invalid credentials",
        )
    isPasswordCorrect = utils.verify_password(
        user.password, user_from_DB.hashed_password
    )
    if not isPasswordCorrect:
        raise HTTPException(
            status_code=404,
            detail="Invalid credentials",
        )

    payload = {"user_id": user_from_DB.id}

    token = await utils.create_jwt_token(payload, timedelta(minutes=int(JWT_EXPIRES)))
    return {"token": token, "user": user_from_DB}


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = await utils.decode_jwt_token(token)
    if not user_id:
        raise utils.credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
