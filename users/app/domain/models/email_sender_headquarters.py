from sqlmodel import SQLModel, Field


class EmailSenderHeadquarters(SQLModel, table=True):
    __tablename__ = "email_sender_headquarters"
    
    sender_id: str = Field(
        foreign_key="email_sender.id",
        primary_key=True, max_length=50
    )
    cod_headquarters: str = Field(
        foreign_key="headquarters.cod_headquarters",
        primary_key=True, max_length=50
    )
