from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel, EmailStr


class UserBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    surname: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)

class Users(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class UserResponse(UserBase):
    id: int

class UsersResponse(BaseModel):
    message: str
    users: List[UserResponse]