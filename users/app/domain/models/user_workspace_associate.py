from sqlmodel import SQLModel, Field


class UserWorkspaceAssociate(
    SQLModel, table=True
):
    __tablename__ = "user_workspace_associate"

    email_unal: str = Field(
        foreign_key="user_unal.email_unal", max_length=100, primary_key=True)
    user_workspace_id: str = Field(
        foreign_key="user_workspace.user_workspace_id",
        max_length=50,
        primary_key=True
    )
    cod_period: str = Field(
        foreign_key="period.cod_period", max_length=50, primary_key=True)
