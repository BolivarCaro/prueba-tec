from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import  get_session
from app.models import User, Message
from app.services.openai_services import get_gpt_response
from pydantic import BaseModel


router = APIRouter()

#Modelo para enviar mensajes
class MessageCreate(BaseModel):
    username: str
    question: str


@router.post("/ask")
def ask(message: MessageCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == message.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    
    try:
        answer = get_gpt_response(message.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    #guarda la conversación el la base de datos
    new_message = Message(user_id=user.id, question=message.question, response=answer)
    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    return { "message": "Pregunta realizada con exito", "response": answer }
    
    