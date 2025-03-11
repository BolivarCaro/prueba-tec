from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")
DATABASE_URL= os.getenv("DATABASE_URL", "sqlite:///./database.db" ) 

if not API_KEY_OPENAI:
    raise ValueError("API_KEY_OPENAI no esta definida en el archivo .env")