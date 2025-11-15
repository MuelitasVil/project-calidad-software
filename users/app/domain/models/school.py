from sqlmodel import SQLModel, Field
from typing import Optional


class School(SQLModel, table=True):
    __tablename__ = "school"

    cod_school: str = Field(primary_key=True, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    type_facultad: Optional[str] = Field(default=None, max_length=50)
