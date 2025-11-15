from sqlmodel import SQLModel, Field


class TypeUserAssociation(SQLModel, table=True):
    __tablename__ = "type_user_association"

    email_unal: str = Field(
        foreign_key="user_unal.email_unal",
        primary_key=True, max_length=100
    )
    type_user_id: str = Field(
        foreign_key="type_user.type_user_id",
        primary_key=True, max_length=50
    )
    cod_period: str = Field(
        foreign_key="period.cod_period",
        primary_key=True, max_length=50
    )
