from sqlmodel import SQLModel, Field


class EmailSenderSchool(SQLModel, table=True):
    __tablename__ = "email_sender_school"

    sender_id: str = Field(
        foreign_key="email_sender.id",
        primary_key=True, max_length=50)
    cod_school: str = Field(
        foreign_key="school.cod_school",
        primary_key=True, max_length=50)
