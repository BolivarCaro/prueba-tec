import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.main import app
from app.core.database import get_session

#Configurar la base de datos en memoria para las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)

#Sobreescribir la dependencia de la sesión para usar la base en memoria
def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

def test_init_success():
    #se envia una solicitud para crear un usuario nuevo
    response = client.post("/init_user", json={"username": "testuser"})
    assert response.status_code == 200, "El estado debe ser 200 ok para un usuario creado"
    data = response.json()
    assert data["username"] == "testuser", "El nombre del usuario debe coincidir"
    #Se verifica que se asigna el rol por defecto de experto en evaluacion de riesgos laborales
    assert data["role"] == "experto en evaluacion de riesgos laborales", "El rol debe ser predeterminado"

def test_init_user_already_exists():
    #primero se crea un usuario
    client.post("/init_user", json={"username": "duplicateuser"})
    #Al intentar crearlo nuevamente se espera un error
    response = client.post("/init_user", json={"username": "duplicateuser"})
    assert response.status_code == 400, "Debe retornar error 400 si el usuario ya existe"
    data = response.json()
    assert data["detail"] == "El usuario ya existe", "El mensaje de error debe indicar que el usuario ya existe"
