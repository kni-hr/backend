from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from database import Base
from schemas.user_schemas  import UserRole

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum(UserRole), default=UserRole.CANDIDATE)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))