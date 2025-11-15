from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class UserWorkspace(SQLModel, table=True):
    __tablename__ = "user_workspace"

    user_workspace_id: str = Field(
        default=None,
        primary_key=True,
        max_length=50
    )
    space: str = Field(max_length=100)
    last_connection: Optional[datetime] = None
    active: bool = True
