from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from sqlmodel import Field, Session, SQLModel, create_engine, select

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from starlette.responses import RedirectResponse


class Candidate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    surname: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    email: str = Field(index=True)
    experience: int = Field(index=True)
    login: str = Field(index=True)
    password: str = Field(index=True)

class HR(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    surname: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    email: str = Field(index=True)
    salary: int = Field(index=True)
    login: str = Field(index=True)
    password: str = Field(index=True)

class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login: str = Field(index=True)
    password: str = Field(index=True)




# PostgreSQL database configuration
postgres_url = "postgresql://postgres:12345678@localhost/postgres"

engine = create_engine(postgres_url)  # No connect_args needed for PostgreSQL


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/candidates/add/")
def create_hero(candidate: Candidate, session: SessionDep) -> Candidate:
    candidate.password = hash_password(candidate.password)
    session.add(candidate)
    session.commit()
    session.refresh(candidate)
    return candidate

@app.get("/",response_class=HTMLResponse)
async def signin(request:Request):
    return templates.TemplateResponse("new_candidate_form.html",context={"request":request})
@app.get("/candidates/")
def read_candidates(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Candidate]:
    candidates = session.exec(select(Candidate).offset(offset).limit(limit)).all()
    return candidates


@app.get("/candidates/{candidate_id}", response_class=HTMLResponse)
async def read_candidate(request: Request, candidate_id: int):
    return templates.TemplateResponse("candidate.html", {"request": request, "id": candidate_id})


@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int, session: SessionDep):
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    session.delete(candidate)
    session.commit()
    return {"ok": True}
