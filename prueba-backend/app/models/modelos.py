from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    role: str
    #relacion con los mensajes (mensajes relacionados con el usuario)
    messages: List["Message"] = Relationship(
        back_populates="user", sa_relationship_kwargs={
            "cascade": "all, delete"
        }
    )

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    question : str
    response: str
    #realcion con la clase User, permite acceder al usuario desde un mensaje
    user: Optional[User] = Relationship(back_populates="messages")