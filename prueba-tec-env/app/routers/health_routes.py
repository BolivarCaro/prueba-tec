from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from database import engine

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """
    Verifica el estado del servicio y la conexión a la base de datos.
    """
    try:
        with Session(engine) as session:
            # Se ejecuta una consulta simple para validar la conexión.
            session.exec("SELECT 1")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la conexión a la base de datos: {str(e)}")
    return {"status": "OK", "database": "connected"}
