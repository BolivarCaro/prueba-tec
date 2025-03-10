import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from main import app
from database import get_session
import openai

# Configurar la base de datos en memoria para pruebas con SQLModel
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SQLModel.metadata.create_all(test_engine)

# Sobreescribir la dependencia get_session para que use la base de datos en memoria
def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

# Creamos clases fake para simular la respuesta de OpenAI, 
# ya que el endpoint espera acceder a response.choices[0]["message"]["content"].text.strip()
class FakeMessage:
    def __init__(self, content: str):
        self.content = content

    @property
    def text(self):
        return self.content

class FakeChoice:
    def __init__(self, content: str):
        self.message = {"content": FakeMessage(content)}

class FakeResponse:
    def __init__(self, content: str):
        self.choices = [FakeChoice(content)]

# Función fake para reemplazar openai.ChatCompletion.create
def fake_chatcompletion_create(*args, **kwargs):
    return FakeResponse("Fake answer from GPT")

def test_ask_endpoint_success(monkeypatch):
    # Primero se crea un usuario para la prueba usando el endpoint /init_user
    init_response = client.post("/init_user", json={"username": "testuser"})
    assert init_response.status_code == 200, "Error al crear el usuario de prueba"
    
    # Reemplazar la función de OpenAI para simular una respuesta
    monkeypatch.setattr(openai.ChatCompletion, "create", fake_chatcompletion_create)
    
    # Llamar al endpoint /ask
    payload = {"username": "testuser", "question": "¿Cuál es el riesgo laboral más común en construcción?"}
    response = client.post("/ask", json=payload)
    
    assert response.status_code == 200, "El endpoint /ask debe retornar 200 en caso de éxito"
    data = response.json()
    assert "response" in data, "La respuesta debe contener la llave 'response'"
    assert data["response"] == "Fake answer from GPT", "La respuesta no coincide con la respuesta fake esperada"

def test_ask_user_not_found():
    # Llamar al endpoint /ask con un usuario que no existe
    payload = {"username": "nonexistent", "question": "¿Cuál es el riesgo laboral más común?"}
    response = client.post("/ask", json=payload)
    
    assert response.status_code == 404, "Debe retornar 404 si el usuario no se encuentra"
    data = response.json()
    assert data["detail"] == "usuario no encontrado", "El mensaje de error debe indicar que el usuario no existe"
