from sqlmodel import SQLModel, Field


class UserUnitAssociate(SQLModel, table=True):
    __tablename__ = "user_unit_associate"

    email_unal: str = Field(
        foreign_key="user_unal.email_unal",
        primary_key=True,
        max_length=100
    )
    cod_unit: str = Field(
        foreign_key=(
            "unit_unal.cod_unit"
        ),
        primary_key=True,
        max_length=50
    )
    cod_period: str = Field(
        foreign_key="period.cod_period",
        primary_key=True,
        max_length=50
    )
