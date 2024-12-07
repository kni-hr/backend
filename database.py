from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from core.config.settings import settings

DATABASE_URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = None
SessionLocal = None 
Base = declarative_base()

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    with engine.connect() as connection:
        connection.execute(text('SELECT 1'))
    print("Database connection successful.")

except OperationalError as e:
    print("Could not connect to the database. Exception: ", e)
    engine = None
    SessionLocal = None