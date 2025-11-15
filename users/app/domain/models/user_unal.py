from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional


class UserUnal(SQLModel, table=True):
    __tablename__ = "user_unal"

    email_unal: str = Field(primary_key=True, max_length=100)
    document: Optional[str] = Field(default=None, max_length=50)
    name: Optional[str] = Field(default=None, max_length=100)
    lastname: Optional[str] = Field(default=None, max_length=100)
    full_name: Optional[str] = Field(default=None, max_length=200)
    gender: Optional[str] = Field(default=None, max_length=10)
    birth_date: Optional[date] = None
