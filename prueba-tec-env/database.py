from sqlmodel import SQLModel, create_engine, Session
from fastapi import HTTPException


DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)


#funcion para inicializar la base de datos
def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inicializar la base de datos: {str(e)}")

#Funcion para obtener una session de base de datos

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()