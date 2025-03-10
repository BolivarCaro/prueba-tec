from sqlmodel import SQLModel, create_engine, Session
from typing import Optional

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)


#funcion para inicializar la base de datos
def init_db():
    SQLModel.metadata.create_all(engine)

#Funcion para obtener una session de base de datos

def get_session():
    with Session(engine) as session:
        yield session