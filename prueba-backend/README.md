# API RESTful Chatbot con FastAPI

## Descripción
Esta aplicación implementa un chatbot configurable con roles utilizando FastAPI y la API gratuita de OpenAI. La aplicación realiza persistencia de datos en SQLite y sigue buenas prácticas de desarrollo, incluyendo modularización del código, manejo de excepciones y pruebas unitarias.

## Estructura del Proyecto

/project-root |-- app | |-- main.py # Archivo principal que inicia la aplicación | |-- core | | -- database.py # Configuración y conexión a la base de datos | |-- models | | |-- user.py # Modelo de datos para los usuarios | | -- message.py # Modelo de datos para los mensajes | -- routers | |-- init_user.py # Endpoint para inicializar usuarios | |-- ask.py # Endpoint para enviar mensajes al chatbot | |-- history.py # Endpoint para consultar el historial | -- health.py # Endpoint para verificar el estado del servicio (nuevo) -- tests -- test_endpoints.py # Pruebas unitarias para los endpoints

## Requisitos
- Python 3.9+
- FastAPI
- SQLModel (o SQLAlchemy)
- Uvicorn
- Pytest
- Pyright (para análisis de tipos)

## Instalación
instalar las dependencias con el siguiente comando con cmd:
py -m pip install -r requirements.txt


1. **Clonar el repositorio:**
Clonar el repositorio en:
   git clone <https://github.com/BolivarCaro/prueba-tec.git>
   cd <prueba-tec>


## Ejecucion
ejecutar la aplicacion en un entorno virtual "uvicorn app.main:app --reload" o
py -m uvicorn app.main:app --reload


## Pruebas unitarias
Ejecutar con el siguiente comando en la consola "pytest"
