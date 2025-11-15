from sqlmodel import SQLModel, Field


class SchoolHeadquartersAssociate(SQLModel, table=True):
    __tablename__ = "school_headquarters_associate"
    
    cod_school: str = Field(
        foreign_key="school.cod_school",
        primary_key=True, max_length=50)
    cod_headquarters: str = Field(
        foreign_key="headquarters.cod_headquarters",
        primary_key=True, max_length=50)
    cod_period: str = Field(
        foreign_key="period.cod_period",
        primary_key=True, max_length=50)
