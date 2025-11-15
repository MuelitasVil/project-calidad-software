from sqlmodel import SQLModel, Field
from typing import Optional


class EmailSender(SQLModel, table=True):
    __tablename__ = "email_sender"

    id: str = Field(primary_key=True, max_length=50)
    email: str = Field(unique=True, max_length=100)
    name: Optional[str] = Field(default=None, max_length=100)
