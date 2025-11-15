from sqlmodel import SQLModel, Field
from datetime import datetime


class SystemUser(SQLModel, table=True):
    __tablename__ = "system_user"

    email: str = Field(primary_key=True, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: str
    state: bool = True
    salt: str = Field(max_length=255)
