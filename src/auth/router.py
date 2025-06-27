from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from . import services, schemas

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


@auth_router.post("/", status_code=201, response_model=schemas.User)
async def login_user(user: schemas.UserAuth, db: Session = Depends(get_db)):
    return services.login_user(
        user,
        db,
    )
