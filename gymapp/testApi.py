import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import date

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
        temperature=0.9,
    )
    return response.choices[0].message.content


def macrosCalc(peso,altura,edad,actividad,meta,genero):
    meta = meta.lower()
    genero = genero.lower()
    if genero == 'male':
        r = ((10* peso)+(6.25*altura)-(5*edad)+5)
    else:
        r = ((10* peso)+(6.25*altura)-(5*edad)-161)
    if actividad == 1 or  actividad == 2 or actividad == 3:
        x = 1.2
    elif actividad == 4 or actividad == 5 or actividad == 6:
        x = 1.375
    elif actividad == 7 or actividad == 8 or actividad == 9:
        x = 1.6
    else:
        x = 1.8
    if meta == 'maximun fat loss':
        meta = 0.8
    elif meta == 'fat loss':
        meta = 0.85
    elif meta == 'some fat loss':
        meta = 0.9
    elif meta == 'mantain':
        meta = 1
    elif meta == 'steady gain':
        meta = 1.1
    elif meta == 'gain':
        meta = 1.2
    r = r*x*meta
    return r

def calcular_edad(fecha):
        today = date.today()
        edad = today.year - fecha.year - ((today.month, today.day) < (fecha.month, fecha.day))
        return edad

