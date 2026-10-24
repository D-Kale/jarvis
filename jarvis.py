import os
from dotenv import load_dotenv
from google import genai

from tools.index import TOOLS
from tools.system import getsysteminfo
from tools.tools import ejecutar_tool

load_dotenv()

# Inicialización
client = genai.Client(api_key=os.getenv("API_KEY"))
MODELO = "gemini-3.5-flash-lite"

info_inicial = getsysteminfo()

SYSTEM_PROMPT = f"""
Eres Jarvis, un asistente virtual inteligente, educado y muy eficiente.

INFORMACIÓN DEL ENTORNO LOCAL:
- Usuario actual: {info_inicial['Usuario Actual']}
- Sistema Operativo: {info_inicial['Sistema Operativo']} (Versión: {info_inicial['Versión del SO']})
- Directorio de usuario por defecto: /home/{info_inicial['Usuario Actual']}

REGLAS DE HERRAMIENTAS:
1. No intentes rutas de Windows (como C:/) si el SO es Linux.
2. Si no te especifican una ruta de búsqueda, usa siempre el directorio del usuario.
3. Piensa los argumentos necesarios antes de llamar una herramienta para acertar al primer intento.
"""

def jarvis(solicitud, historial=None, max_steps=5, verbose=True):
    
    if historial is None:
        historial = []

    config_bus = {
        "tools": [{"function_declarations": [t["function"] for t in TOOLS]}],
        "system_instruction": SYSTEM_PROMPT,
        "temperature": 0.2
    }

    chat = client.chats.create(
        model=MODELO,
        config=config_bus,
        history=historial
    )

    response = enviar_mensaje_con_reintento(chat, solicitud)

    for paso in range(max_steps):
        # Verificar si hay llamadas a funciones
        func_calls = [part.function_call for part in response.candidates[0].content.parts if part.function_call]

        if not func_calls:
            return response.text, chat.get_history()

        # Procesar cada llamada a función
        respuestas_tool = []
        for fc in func_calls:
            nombre = fc.name
            argumentos = fc.args
            resultado = ejecutar_tool(nombre, argumentos)

            if verbose:
                print(f"🔧 Tool llamada: {nombre}")
                print(f"📥 Argumentos: {argumentos}")
                print(f"📤 Resultado: {resultado}\n")

            # Crear respuesta de la función para el modelo
            response_dict = resultado if isinstance(resultado, dict) else {"result": resultado}

            respuestas_tool.append(genai.types.Part.from_function_response(
                name=nombre,
                response=response_dict
            ))

        # Enviar los resultados de vuelta al modelo
        response = enviar_mensaje_con_reintento(chat, respuestas_tool)

    return "El agente alcanzó el máximo de pasos.", chat.history

import time
from google.genai.errors import APIError, ServerError

def enviar_mensaje_con_reintento(chat, contenido, max_reintentos=3):
    for intento in range(max_reintentos):
        try:
            return chat.send_message(contenido)
        except (ServerError, APIError) as e:
            if intento == max_reintentos - 1:
                raise e
            time.sleep(2 * (intento + 1)) # Espera 2s, luego 4s antes de reintentar