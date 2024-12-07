from fastapi import FastAPI
from database import engine, Base
from routers.user_router import router as user_router
from routers.auth_router import router as auth_router

app = FastAPI()

if engine is not None:
    Base.metadata.create_all(bind=engine)


app.include_router(user_router, prefix="/api/v1", tags=["Users"])
app.include_router(auth_router, tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the HR Management API!"}