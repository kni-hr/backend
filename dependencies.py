from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from database import Session

def get_db_session():
    if Session is None:
        raise RuntimeError("Database connection is not available.")

    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()

SessionDep = Annotated[Session, Depends(get_db_session)]