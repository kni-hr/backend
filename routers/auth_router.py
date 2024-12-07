from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user_schema import Token, UserCreate
from services.auth_service import AuthService
from dependencies import get_db
from core.exceptions.auth_exceptions import InvalidCredentials, UserAlreadyExists

router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db),
):
    try:
        return await AuthService.login(form_data, db)
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_form: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return await AuthService.register(user_form, db)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )