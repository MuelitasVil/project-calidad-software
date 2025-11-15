from sqlmodel import SQLModel, Field
from typing import Optional


class UnitUnal(SQLModel, table=True):
    __tablename__ = "unit_unal"

    cod_unit: str = Field(primary_key=True, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    type_unit: Optional[str] = Field(default=None, max_length=50)
