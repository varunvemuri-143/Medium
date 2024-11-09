from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr]
    user_type: Optional[str] = "base"
    status: Optional[str] = "active"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashedPassword: str
