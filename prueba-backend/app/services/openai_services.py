import openai
import os
from app.core.config import API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI

def get_gpt_response(user_message: str) -> str:
    """
    envia un mensaje a OpenAII GPT y obtiene una respuesta.

    args:
        user_name (str): La pregunta del usuario
    returns:
        str: la respuesta generada por GPT

    """
    system_message = {"role": "system", "content": "Eres un experto en riesgos laborales."}
    user_message = {"role": "user", "content": message.question}

    try:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message, user_message],
            temperature = 0.7
        )

        answer = response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"Error en OpenAI: {str(e)}")
