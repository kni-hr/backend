from fastapi import APIRouter, Query, Depends, status, HTTPException
from schemas.user_schemas import User, UserCreate, UserRead, UserUpdate
from typing import Annotated
from dependencies import SessionDep, get_db_session
from models.user_model import User as User_DB
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate, session: Session = Depends(get_db_session)) :
    user = User_DB(name=request.name, surname=request.surname, password=request.password, email=request.email)
    session.add(user)
    session.commit()    
    session.refresh(user)
    return request

@router.get("/users/{user_id}")
async def get_user(session: SessionDep ,user_id: int) -> User :
    user = session.get(User_DB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model = list[UserRead])
async def get_users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return session.query(User_DB).offset(offset).limit(limit).all()

@router.patch("/users/{user_id}")
async def patch_user(user_id: int, updates: UserUpdate, session: SessionDep):
    user = session.get(User_DB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    session.commit()
    session.refresh(user)
    return {"message": "User updated successfully", "user": user}

@router.delete("/users/{user_id}")
async def delete_user(session: SessionDep ,user_id: int):
    user = session.get(User_DB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}