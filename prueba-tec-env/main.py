from fastapi import FastAPI
from database import init_db
from app.routers import router
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("API_KEY_OPENAI")

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)