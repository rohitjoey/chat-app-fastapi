from sqlalchemy.orm import Session
from . import models, schemas
from . import utils
from fastapi import HTTPException, status


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


def login_user(
    user: schemas.UserAuth,
    db: Session,
):
    user_data = user.model_dump()
    user = get_user_by_email(user_data["email"], db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Invalid credentials",
        )

    isPasswordCorrect = utils.verify_password(
        user_data["password"], user.hashed_password
    )
    if not isPasswordCorrect:
        raise HTTPException(
            status_code=404,
            detail="Invalid credentials",
        )
    return user
