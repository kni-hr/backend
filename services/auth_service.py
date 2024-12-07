from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from schemas.user_schema import Token
from models import User
from schemas.user_schema import UserCreate
from repositories.user_repository import UserRepository
from utils.jwt_handler import create_access_token
from core.exceptions.auth_exceptions import InvalidCredentials, UserAlreadyExists

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @classmethod
    async def login(cls, form_data: OAuth2PasswordRequestForm, db: Session) -> Token:
        # Fetch user from the database
        user: User = UserRepository.get_user_by_username(db, form_data.username)
        if not user or not pwd_context.verify(form_data.password, user.password):
            raise InvalidCredentials()
        
        # Generate token
        access_token = create_access_token({"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")
    
    @classmethod
    async def register(cls, user_form: UserCreate, db: Session):
        # Check if user already exists
        if UserRepository.get_user_by_username(db, user_form.email):
            raise UserAlreadyExists()
        
        # Create user
        db_user = User(
            name=user_form.name, 
            surname=user_form.surname,
            email=user_form.email, 
            password=pwd_context.hash(user_form.password))
        
        UserRepository.create_user(db, db_user)
        return {"message": "User created successfully"}