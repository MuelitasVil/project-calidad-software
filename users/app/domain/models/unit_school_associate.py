from sqlmodel import SQLModel, Field


class UnitSchoolAssociate(SQLModel, table=True):
    __tablename__ = "unit_school_associate"

    cod_unit: str = Field(
        foreign_key="unit_unal.cod_unit",
        primary_key=True,
        max_length=50
    )
    cod_school: str = Field(
        foreign_key="school.cod_school",
        primary_key=True,
        max_length=50
    )
    cod_period: str = Field(
        foreign_key="period.cod_period",
        primary_key=True,
        max_length=50
    )
