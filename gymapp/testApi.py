import os
from openai import OpenAI
from dotenv import load_dotenv

#Se lee del archivo .env la api key de openai
load_dotenv()

# Obtener la clave de API de OpenAI desde las variables de entorno
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Inicializar el cliente de OpenAI con la clave de API
client = OpenAI(api_key=OPENAI_API_KEY)

#Se carga la lista de películas de movie_titles.json



#Se genera una función auxiliar que ayudará a la comunicación con la api de openai
#Esta función recibe el prompt y el modelo a utilizar (por defecto gpt-3.5-turbo)
#devuelve la consulta hecha a la api

def get_completion(prompt, model="gpt-3.5-turbo",client=client):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content
