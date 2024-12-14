from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserRole(Enum):
    ADMIN = "admin"
    HR = "hr"
    CANDIDATE = "candidate"

class User(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    role: UserRole
    password: str

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]