from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from schemas.user_schema import UserCurrent
from repositories.user_repository import UserRepository
from database import SessionLocal
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from core.config.settings import settings
from core.exceptions.auth_exceptions import TokenException


# Database Dependency
def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database connection is not available.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserCurrent:

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise TokenException
    except JWTError:
        raise TokenException
    
    user = UserRepository.get_user_by_username(db, email)
    if user is None:
        raise TokenException
    return user
    