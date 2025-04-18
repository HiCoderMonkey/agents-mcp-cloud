from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from .base import BaseSchema


class UserBase(BaseSchema):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_admin: bool = False
    username: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str
    username: str


class UserUpdate(BaseSchema):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserInDBBase(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str 