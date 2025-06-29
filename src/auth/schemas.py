from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserAuth(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int
    class Config:
        from_attributes = True


class UserWithToken(BaseModel):
    token: str
    user: User
