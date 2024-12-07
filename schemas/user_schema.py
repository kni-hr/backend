from typing import Optional
from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    password: str
    role: str # Admin, HR, Candidate

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserDisplay(BaseModel):
    name: str
    surname: str
    email: str
    role: str

class UserCurrent(BaseModel):
    name: str
    surname: str
    email: str
    role: str

class UserFilter(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
