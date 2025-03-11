from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models import User
from pydantic import BaseModel, StringConstraints
from typing import Annotated

router = APIRouter()

#modelo para crear usuario
class UserCreate(BaseModel):
    username : Annotated[
        str,
        StringConstraints(min_length=3, max_length=20, pattern="^[a-zA-Z0-9_-]+$")
    ]
    role: str



@router.post("/init_user")
def init_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    try:

        new_user = User(username=user.username, role=user.role)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    return{"message": "Usuario creado satisfactoriamente", "user": new_user}