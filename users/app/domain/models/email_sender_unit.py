from sqlmodel import SQLModel, Field


class EmailSenderUnit(SQLModel, table=True):
    __tablename__ = "email_sender_unit"

    sender_id: str = Field(
        foreign_key="email_sender.id",
        primary_key=True, max_length=50)
    cod_unit: str = Field(
        foreign_key="unit_unal.cod_unit",
        primary_key=True, max_length=50)
