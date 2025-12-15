import os

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
pswrd = os.getenv("PASS")
engine = create_async_engine(f'postgresql+asyncpg://postgres:{pswrd}@localhost:5555/bd_try')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "main"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    ph_num: Mapped[str]


class ContactAddSchema(BaseModel):
    name: str
    ph_num: str


class ContactSchema(BaseModel):
    id: int


@app.post("/contacts")
async def add_contact(data: ContactAddSchema, session: SessionDep):
    new_contact = Contact(
        name=data.name,
        ph_num=data.ph_num
    )
    session.add(new_contact)
    await session.commit()
    return {'success': True}


@app.get("/contacts")
def get_contact():
    pass

if __name__ == "__main__":
    uvicorn.run("database_fastapi:app", reload=True)