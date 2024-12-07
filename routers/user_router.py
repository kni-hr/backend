from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user_schema import UserDisplay, UserFilter, UserCurrent
from sqlalchemy.orm import Session
from dependencies import get_current_user, get_db
from core.exceptions.user_exceptions import PermissionException, UserNotFoundException, UserCannotBePromotedException, UserCannotBeDemotedException
from services.user_service import UserService

router = APIRouter()

@router.get("/users", response_model=List[UserDisplay])
async def get_users(
    filter_form: UserFilter = Depends(),
    current_user: UserCurrent = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return await UserService.get_users(db, filter_form, current_user)
    except PermissionException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to list users")


@router.put("/users/promote/{user_id}")
async def promote_user(
    user_id: int,
    current_user: UserCurrent = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        await UserService.promote_user(db, user_id, current_user)
        return {"message": "User promoted successfully"}
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to promote users")
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except UserCannotBePromotedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already an HR employee")


@router.put("/users/demote/{user_id}")
async def demote_user(
    user_id: int,
    current_user: UserCurrent = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        await UserService.demote_user(db, user_id, current_user)
        return {"message": "User demoted successfully"}
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to demote users")
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except UserCannotBeDemotedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a candidate")


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserCurrent = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        await UserService.delete_user(db, user_id, current_user)
        return {"message": "User deleted successfully"}
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete users")
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
