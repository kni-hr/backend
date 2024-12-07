from sqlalchemy.orm import Session
from schemas.user_schema import UserFilter
from models import User

class UserRepository:
    @staticmethod
    def get_user_by_username(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)

    @staticmethod
    def get_filtered_users(db: Session, filters: UserFilter, current_user_id: int):
        query = db.query(User)
        
        if filters.name:
            query = query.filter(User.name.contains(filters.name))
        if filters.surname:
            query = query.filter(User.surname.constraints(filters.surname))
        if filters.email:
            query = query.filter(User.email.contains(filters.email))
        if filters.role:
            query = query.filter(User.role == filters.role)
        
        query = query.filter(User.id != current_user_id)

        return query.all()
    
    @staticmethod
    def get_filtered_users_for_hr(db: Session, filters: UserFilter):
        query = db.query(User).filter(User.role == "Candidate")
        
        if filters.name:
            query = query.filter(User.name.contains(filters.name))
        if filters.surname:
            query = query.filter(User.surname.contains(filters.surname))
        if filters.email:
            query = query.filter(User.email.contains(filters.email))
        
        return query.all()
    
    @staticmethod
    def promote_user(db: Session, db_user: User):
        db_user.role = "HR"
        db.commit()
        db.refresh(db_user)
        
    @staticmethod
    def demote_user(db: Session, db_user: User):
        db_user.role = "Candidate"
        db.commit()
        db.refresh(db_user)

    @staticmethod
    def delete_user(db: Session, db_user: User):
        db.delete(db_user)
        db.commit()
    
