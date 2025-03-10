import openai
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import  get_session
from app.models import User, Message
from pydantic import BaseModel

router = APIRouter()

#Modelo para enviar mensajes
class MessageCreate(BaseModel):
    username: str
    question: str

openai.api_key = "API_KEY_OPENAI"

@router.post("/ask")
def ask(message: MessageCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == message.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    #Rol del GPT
    system_message = {
        "role": "system",
        "content": "Eres un experto en evaluación de riesgos laborales."
    }
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[ system_message, #se agrega el contexto del rol
                  {"role": "user", "content": message.question}
                  ],
        max_tokens=150
    )

    response_text = response.choices[0]["message"]["content"].text.strip()

    #guarda la conversación el la base de datos
    new_message = Message(user_id=user.id, question=message.question, response=response_text)
    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    return { "message": "Pregunta realizada con exito", "response": response_text }
    
    