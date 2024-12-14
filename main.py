from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from database  import Base, engine
from contextlib import asynccontextmanager
from routers.user_router import router as user_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_db_and_tables():
    Base.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["Users"])

@app.get("/")
async def home():
    return {"message": "Hello, HR!"}