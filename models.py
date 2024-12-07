from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from database import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    role = Column(String, default="Candidate")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
