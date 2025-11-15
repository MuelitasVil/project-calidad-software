from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

print(f"Connecting to database at {DATABASE_URL}")

# El engine es exactamente el mismo
engine = create_engine(DATABASE_URL, echo=True)


# Crear tablas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Proveer sesiones como dependencia
def get_session():
    with Session(engine) as session:
        yield session
