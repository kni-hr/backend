from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from schemas.user_schema import UserFilter, UserCurrent, UserDisplay
from core.exceptions.user_exceptions import (
    PermissionException, 
    UserNotFoundException, 
    UserCannotBePromotedException, 
    UserCannotBeDemotedException,
    InvalidPaginationParams,
    )
from typing import List

class UserService:
    @classmethod
    async def get_users(cls, db: Session, filter_form: UserFilter, current_user: UserCurrent, offset: int, limit: int) -> List[UserDisplay]:
       if current_user.role == "Candidate":
           raise PermissionException
       
       if offset < 0 or limit < 0:
           raise InvalidPaginationParams
       
       if current_user.role == "HR":
            users = UserRepository.get_filtered_users_for_hr(db, filter_form)
            if offset + limit > len(users):
                return users[offset:]

            return users[offset:offset+limit]
       
       else:
            users = UserRepository.get_filtered_users(db, filter_form, current_user.id)
            if offset + limit > len(users):
                return users[offset:]
            
            return users[offset:offset+limit]
           
           
    
    @classmethod
    async def promote_user(cls, db: Session, user_id: int, current_user: UserCurrent):
        if current_user.role != "Admin":
            raise PermissionError
        
        existing_user = UserRepository.get_user_by_id(db, user_id)

        if existing_user is None:
            raise UserNotFoundException
        
        if existing_user.role == "HR":
            raise UserCannotBePromotedException
        
        UserRepository.promote_user(db, existing_user)

    @classmethod
    async def demote_user(cls, db: Session, user_id: int, current_user: UserCurrent):
        if current_user.role != "Admin":
            raise PermissionError
        
        existing_user = UserRepository.get_user_by_id(db, user_id)

        if existing_user is None:
            raise UserNotFoundException
        
        if existing_user.role == "Candidate":
            raise UserCannotBeDemotedException
        
        UserRepository.demote_user(db, existing_user)

    @classmethod
    async def delete_user(cls, db: Session, user_id: int, current_user: UserCurrent):
        if current_user.role != "Admin":
            raise PermissionError
        
        existing_user = UserRepository.get_user_by_id(db, user_id)

        if existing_user is None:
            raise UserNotFoundException
        
        UserRepository.delete_user(db, existing_user)