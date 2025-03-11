from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import  get_session
from app.models import User, Message
from pydantic import BaseModel

router = APIRouter()

# Modelo para acceder al historial del usuario
@router.get("/history/{username}")
def get_history(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    messages = session.exec(select(Message).where(Message.user_id == user.id)).all()
    return {"messages": messages}